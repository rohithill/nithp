import connexion
from flask import url_for
import sqlite3
import time

def query_db(query, args=tuple(), one=False,limit=0):
    conn = sqlite3.Connection('file:nithResult.db?mode=ro',uri=True)
    conn.row_factory = sqlite3.Row
    # print(query,args)
    cur = conn.execute(query, args)
    rv = cur.fetchmany(limit)
    conn.close()
    
    return (rv[0] if rv else None) if one else rv

def read_all():
    name = connexion.request.args.get('name') or ''
    branch = connexion.request.args.get('branch')
    roll = connexion.request.args.get('roll') or '%'
    subject_code = connexion.request.args.get('subject_code') or '%'
    min_cgpi = float(connexion.request.args.get('min_cgpi') or 0)
    max_cgpi = float(connexion.request.args.get('max_cgpi') or 10)
    min_sgpi = float(connexion.request.args.get('min_sgpi') or 0)
    max_sgpi = float(connexion.request.args.get('max_sgpi') or 10)
    next_cursor = connexion.request.args.get('next_cursor','0')
    limit = int(connexion.request.args.get('limit',10))

    limit = min(max(1,limit),5000)

    st = time.time()

    data = {
        'name': name,
        'branch' : branch,
        'roll': roll,
        'subject_code': subject_code,
        'min_cgpi': min_cgpi,
        'max_cgpi': max_cgpi,
        'min_sgpi': min_sgpi,
        'max_sgpi': max_sgpi,
        'limit': limit+1,
        'next_cursor': next_cursor
    }
    if branch:
        result = query_db('''SELECT * from student  
        WHERE (INSTR(LOWER(name),LOWER(TRIM((:name)))) > 0 OR LENGTH(:name) = 0) 
        AND roll like (:roll) 
        AND LOWER(branch)=LOWER(:branch) 
        AND cgpi BETWEEN (:min_cgpi) AND (:max_cgpi) 
        AND sgpi BETWEEN (:min_sgpi) AND (:max_sgpi) 
        AND roll IN (Select roll from result where subject_code like (:subject_code)) 
        AND roll >= (:next_cursor) ORDER BY roll LIMIT (:limit)''',data)
    else:
        result = query_db('''SELECT * from student 
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

    # print(f"Total time elapsed read_all = {time.time() - st}")
    next_cursor = result[-1]["roll"] if len(result) > limit else ''

    return {
        "data":response,
        "pagination": {
            "next_cursor" : next_cursor,
        }
    }

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
def read_subjects():
    if subject_list:
        return subject_list
    
    result = query_db("SELECT distinct subject_code,subject,sub_point from result")
    for row in result:
        subject_list.append({
            i:row[i] for i in row.keys()
        })
    return subject_list
