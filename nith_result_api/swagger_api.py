import connexion
from flask import url_for

import time

from .utils import check_and_set_default, query_db, hit_counter
from utils import timer
from cache import cache

@timer('API read')
@hit_counter('NITH_RESULT_API')
@hit_counter('NITH_RESULT_API_READ')
@cache.cached(timeout=600,query_string=True)
@hit_counter('NITH_RESULT_API_READ_DATABASE')
def read(roll):
    data = {
        "branch": None,
        "cgpi": None,
        "name": None,
        "rank": {
            "class": {
            "cgpi": None,
            "sgpi": None
            },
            "college": {
            "cgpi": None,
            "sgpi": None
            },
            "year": {
            "cgpi": None,
            "sgpi": None
            }
        },
        "result": [],
        "roll": None,
        "sgpi": None,
        "summary": []
    }
    result = query_db('''SELECT roll,
        name,
        branch,
        cgpi,
        sgpi,
        rank_college_cgpi,
        rank_college_sgpi,
        rank_year_cgpi,
        rank_year_sgpi,
        rank_class_cgpi,
        rank_class_sgpi
        FROM student where roll=(?)''',(roll,),one=True,limit=1)

    if not result:
        return {"status": "not found"},404

    for key in result.keys():
        if key.startswith('rank'):
            new_key = key.split('_')
            data[new_key[0]][new_key[1]][new_key[2]] = result[key]
        else:
            data[key] = result[key]

    result = query_db('''SELECT
        grade,
        sem,
        sub_gp,
        sub_point,
        subject,
        subject_code
        FROM result where roll=(?)''',(roll,))

    for row in result:
        data['result'].append({i:row[i] for i in row.keys()})

    result = query_db('''SELECT sem,cgpi,sgpi,cgpi_total,sgpi_total from summary where roll=(?)''',(roll,))
    data['summary'] = [{i:row[i] for i in row.keys()} for row in result]

    return data


@timer('API read_all')
@hit_counter('NITH_RESULT_API')
@hit_counter('NITH_RESULT_API_READ_ALL')
@cache.cached(timeout=600,query_string=True)
@hit_counter('NITH_RESULT_API_READ_ALL_DATABASE')
def read_all():
    args = ('name','branch','roll','subject_code','min_cgpi','max_cgpi','min_sgpi','max_sgpi','next_cursor','limit','sort_by_cgpi')
    data = {}
    for arg in args:
        data[arg] = connexion.request.args.get(arg)
    return get_all_data(data)

def get_all_data(data,exceptional_limit=False):
    check_and_set_default(data)
    if exceptional_limit:
        data['limit'] = 5000
    limit = data['limit']
    data['limit'] += 1

    branch_parameter = 'AND LOWER(branch)=LOWER(:branch)' if data['branch'] else ''
    sort_parameter = 'roll'
    if data['sort_by_cgpi']:
        # ROW_NUMBER() is available on sqlite >= 3.25.0, I have tested it on 3.28.0
        # Heroku currently has 3.22.0, hence it will not work on heroku as of now.
        # In that case providing following implementation.
        sort_parameter = 'rank_college_cgpi'
        # data['next_cursor'] = int(data['next_cursor'])

    result = query_db(f'''
            SELECT * from student
            WHERE (INSTR(LOWER(name),LOWER(TRIM((:name)))) > 0 OR LENGTH(:name) = 0)
            AND roll like (:roll)
            {branch_parameter}
            AND cgpi BETWEEN (:min_cgpi) AND (:max_cgpi)
            AND sgpi BETWEEN (:min_sgpi) AND (:max_sgpi)
            AND roll IN (Select roll from result where subject_code like (:subject_code))
            AND {sort_parameter} >= (:next_cursor)
            order by {sort_parameter} LIMIT (:limit);''',data)

    response = []
    for row in result[:limit]:
        response.append({
            'name': row['name'],
            'roll': row['roll'],
            'branch': row['branch'],
            'cgpi': row['cgpi'],
            'sgpi': row['sgpi'],
            'rank': {
                'college': {
                    'cgpi': row['rank_college_cgpi'],
                    'sgpi': row['rank_college_sgpi']
                },
                'year': {
                    'cgpi': row['rank_year_cgpi'],
                    'sgpi': row['rank_year_sgpi']
                },
                'class': {
                    'cgpi': row['rank_class_cgpi'],
                    'sgpi': row['rank_class_sgpi']
                }
            },
            "link" : connexion.request.path + '/'  + row['roll']
        })

    next_cursor = result[-1][sort_parameter] if len(result) > limit else ''

    return {
        "data":response,
        "pagination": {
            "next_cursor" : str(next_cursor),
        }
    }


subject_list = []
@timer('API read_subjects')
@hit_counter('NITH_RESULT_API')
def read_subjects():
    if subject_list:
        return subject_list

    result = query_db("SELECT distinct subject_code,subject,sub_point from result")
    for row in result:
        subject_list.append({
            i:row[i] for i in row.keys()
        })
    return subject_list

@timer('GET_BRANCHES')
@cache.cached(timeout=24*60*60)
def get_branches():
    result = query_db("SELECT name,starting_batch,latest_batch from branch")
    res = []
    for name,starting_batch,latest_batch in result:
        res.append(
            {
                'name': name,
                'batches':[i for i in range(starting_batch,latest_batch+1)]
            }
        )
    return res

@cache.cached(timeout=24*60*60)
def get_result_updated_date():
    result = query_db("SELECT created_on from meta_info")
    return result[0][0]