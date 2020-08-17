import connexion
from flask import url_for

import time

from .utils import check_and_set_default, query_db, hit_counter, Timer

@hit_counter
def read_all():
    args = ('name','branch','roll','subject_code','min_cgpi','max_cgpi','min_sgpi','max_sgpi','next_cursor','limit','sort_by_cgpi')
    data = {}
    for arg in args:
        data[arg] = connexion.request.args.get(arg)

    with Timer("get_all_data"):
        resp = get_all_data(data)

    return resp

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
        data['next_cursor'] = int(data['next_cursor'])

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

@hit_counter
def read(roll):
    st = time.time()
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

    print(f"Total time elapsed read(roll) = {time.time() - st}")

    return data

subject_list = []
@hit_counter
def read_subjects():
    if subject_list:
        return subject_list

    result = query_db("SELECT distinct subject_code,subject,sub_point from result")
    for row in result:
        subject_list.append({
            i:row[i] for i in row.keys()
        })
    return subject_list

