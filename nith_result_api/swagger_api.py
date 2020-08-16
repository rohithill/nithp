import connexion
from flask import url_for

import sqlite3
import time
from functools import wraps
import urllib.request
import os
import threading

def query_db(query, args=tuple(), one=False,limit=0):
    conn = sqlite3.connect('file:nithResult.db?mode=ro',uri=True)
    conn.row_factory = sqlite3.Row
    # print(query,args)
    cur = conn.execute(query, args)
    rv = cur.fetchmany(limit)
    conn.close()
    
    return (rv[0] if rv else None) if one else rv

def make_request():
    url = os.getenv('COUNT_API_URL') or 'https://api.countapi.xyz/hit/nithp/NITH_RESULT_API'
    req = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req,timeout=5)

def hit_counter(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            threading.Thread(target=make_request).start()
        except Exception as e:
            print("Counter update failed ", e)
        finally:
            return func(*args,**kwargs)
    return wrapper

@hit_counter    
def read_all():
    args = ('name','branch','roll','subject_code','min_cgpi','max_cgpi','min_sgpi','max_sgpi','next_cursor','limit','sort_by_cgpi')
    data = {}
    # print(connexion.request.args)
    for arg in args:
        data[arg] = connexion.request.args.get(arg)
    # print(data)
    st = time.perf_counter()
    resp = get_all_data(data)
    et = time.perf_counter()

    print('Time taken to get_all_data: ',et - st)
    return resp
    # return get_all_data(data)

def get_all_data(data):
    check_and_set_default(data)
    limit = data['limit']
    data['limit'] += 1

    if data['sort_by_cgpi']:
        data['next_cursor'] = int(data['next_cursor'])
        if data['branch']:
            result = query_db(f'''SELECT * FROM (
                SELECT *,row_number() over (order by cgpi desc) ROW_NUM from student  
                WHERE (INSTR(LOWER(name),LOWER(TRIM((:name)))) > 0 OR LENGTH(:name) = 0) 
                AND roll like (:roll)
                AND LOWER(branch)=LOWER(:branch) 
                AND cgpi BETWEEN (:min_cgpi) AND (:max_cgpi) 
                AND sgpi BETWEEN (:min_sgpi) AND (:max_sgpi) 
                AND roll IN (Select roll from result where subject_code like (:subject_code))
            ) t WHERE ROW_NUM >= (:next_cursor) LIMIT (:limit)''',data)
        else:
            result = query_db(f'''SELECT * FROM (
                SELECT *,row_number() over (order by cgpi desc) ROW_NUM from student  
                WHERE (INSTR(LOWER(name),LOWER(TRIM((:name)))) > 0 OR LENGTH(:name) = 0) 
                AND cgpi BETWEEN (:min_cgpi) AND (:max_cgpi) 
                AND sgpi BETWEEN (:min_sgpi) AND (:max_sgpi) 
                AND roll IN (Select roll from result where subject_code like (:subject_code))
                AND roll like (:roll)
            ) t WHERE ROW_NUM >= (:next_cursor) LIMIT (:limit)''',data)
    else:
        if data['branch']:
            result = query_db(f'''SELECT * from student  
            WHERE (INSTR(LOWER(name),LOWER(TRIM((:name)))) > 0 OR LENGTH(:name) = 0) 
            AND roll like (:roll) 
            AND LOWER(branch)=LOWER(:branch) 
            AND cgpi BETWEEN (:min_cgpi) AND (:max_cgpi) 
            AND sgpi BETWEEN (:min_sgpi) AND (:max_sgpi) 
            AND roll IN (Select roll from result where subject_code like (:subject_code)) 
            AND roll >= (:next_cursor) ORDER BY roll LIMIT (:limit)''',data)
        else:
            result = query_db(f'''SELECT * from student 
            WHERE (INSTR(LOWER(name),LOWER(TRIM((:name)))) > 0  OR LENGTH(:name) = 0) 
            and roll like (:roll)  
            AND cgpi BETWEEN (:min_cgpi) AND (:max_cgpi) 
            AND sgpi BETWEEN (:min_sgpi) AND (:max_sgpi) 
            AND roll IN (Select roll from result where subject_code like (:subject_code)) 
            AND roll >= (:next_cursor) ORDER BY roll LIMIT (:limit)''',data)
 
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
    if data['sort_by_cgpi']:
        next_cursor = result[-1]["row_num"] if len(result) > limit else ''
    else:
        next_cursor = result[-1]["roll"] if len(result) > limit else ''


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

def check_and_set_default(data):
    MAX_ROWS_LIMIT = 1000

    defaults = {
        'name' : '',
        'branch' : None,
        'roll' : '%',
        'subject_code' : '%',
        'min_cgpi' : 0,
        'max_cgpi' : 10,
        'min_sgpi' : 0,
        'max_sgpi' : 10,
        'sort_by_cgpi': False,
        'limit' : 50,
        'next_cursor' : 0,
    }
    validate = {
        'name' : lambda x: x or defaults['name'],
        'branch' : lambda x: x.upper() if x else defaults['branch'],
        'roll' : lambda x: x.upper() if x else defaults['roll'],
        'subject_code': lambda x: x.upper() if x else defaults['subject_code'],
        'min_cgpi' : lambda x: float(x) if x and 0 <= float(x) <= 10 else defaults['min_cgpi'],
        'max_cgpi' : lambda x: float(x) if x and 0 <= float(x) <= 10 else defaults['max_cgpi'],
        'min_sgpi' : lambda x: float(x) if x and 0 <= float(x) <= 10 else defaults['min_sgpi'],
        'max_sgpi' : lambda x: float(x) if x and 0 <= float(x) <= 10 else defaults['max_sgpi'],
        'sort_by_cgpi' : lambda x: x and x.lower() == 'true',
        'limit' : lambda x: int(x) if x and int(x) > 0 and int(x) <= MAX_ROWS_LIMIT else defaults['limit'],
        'next_cursor' : lambda x: x or defaults['next_cursor'],
    }
    assert defaults.keys() == validate.keys(), 'For every arg there must exists a default value and validation function. One of them is missing.'

    for prop in validate:
        data[prop] = validate[prop](data.get(prop))
