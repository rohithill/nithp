from flask import Blueprint, jsonify, request
from flask_cors import CORS
import sqlite3

api = Blueprint('api',__name__)

# CORS(api)

@api.route('/')
def home():
    return jsonify({"Status":1})

@api.route('/search')
def search():
    rollno = request.args.get('rollno')
    name = request.args.get('name')
    mincgpi = request.args.get('mincgpi')
    maxcgpi = request.args.get('maxcgpi')

    return jsonify(find_result(rollno,name,mincgpi,maxcgpi))

@api.route('/result/<string:rollno>/')
@api.route('/result/<string:rollno>/<int:sem>')
def getresult(rollno,sem=None):
    response = get_single_result(rollno,sem)
    return jsonify(response)

results = {}
import os, json
def init():
    for root, subFolder, files in os.walk('result'):
        for item in files:
            if item.endswith(".json") :
                fileNamePath = str(os.path.join(root,item))
                with open(fileNamePath,'r') as f:
                    data = json.loads(f.read())
                    for r in data:
                        results[r['roll']] = r
                        
                        # perform modification
                        
                        temp_list = []
                        for sem in r['result']:
                            if sem == 'head':
                                continue
                            for sub in r['result'][sem]:
                                temp_dict = {}
                                for i,j in zip(r['result']['head'],sub):
                                    temp_dict[i.lower()] = j
                                temp_dict['sem'] = str(int(sem[1:]))
                                temp_list.append(temp_dict)
                        r['result'] = temp_list

                        # change summary
                        temp_list = []
                        for sem in r['summary']:
                            if sem == 'head':       
                                continue
                            temp_dict = {}
                            for i,j in zip(r['summary']['head'],r['summary'][sem]):
                                temp_dict[i.lower()] = j
                            temp_dict['sem'] = str(int(sem[1:]))
                            temp_list.append(temp_dict)  
                        r['summary'] = temp_list
init()   
import time
# from cache import cache
# @cache.cached(timeout=5,query_string=True)

def query_db(query, args=tuple(), one=False,limit=0):
    conn = sqlite3.Connection('file:nithResult.db?mode=ro',uri=True)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(query, args)
    rv = cur.fetchmany(limit)
    conn.close()
    
    return (rv[0] if rv else None) if one else rv

def read_all():
    st = time.time()
    # print(locals(), len(globals()),globals().keys(),request.path,request.endpoint)
    

    # cur.execute('''SELECT * from student''')
    # result = cur.fetchmany(200)
    result = query_db('SELECT * from student')
    # print(result.keys())
    response = []
    for row in result:
        # print(row.keys())
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
            "link" : request.path + '/'  + row['roll']
        })

    print(f"Total time elapsed read_all = {time.time() - st}")
    return response

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
    # result = cur.fetchone()

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

def find_result(rollno=None,name=None,mincgpi=0,maxcgpi=10):
    if not rollno:
        rollno = '%'
    if not name:
        name = ''
    if not mincgpi:
        mincgpi = 0
    if not maxcgpi:
        maxcgpi = 10

    mincgpi = float(mincgpi)
    maxcgpi = float(maxcgpi)

    import time
    st = time.perf_counter()
    diff = lambda: time.perf_counter() - st
    response_array = {
    'head':('rollno','name','cgpi'),
    'body':[]}
    conn = sqlite3.connect('file:nithResult.db?mode=ro',uri=True)
    print('Created connnection: ',diff())
    # print(conn.execute('SELECT LENGTH('ROHIT');').fetchall())
    # print('name',name,repr(name))
    # print(conn.execute('''SELECT LENGTH(:name);''',{'name':name}).fetchall())
    result = conn.execute('SELECT rollno,name,cgpi FROM student NATURAL JOIN cgpi \
    WHERE (INSTR(LOWER(name),LOWER(TRIM((:name)))) > 0 OR LENGTH(:name) = 0) AND rollno LIKE (:rollno) AND cgpi >= (:mincgpi) AND cgpi <= (:maxcgpi)',
    {'name':name,'rollno':rollno,'mincgpi':mincgpi,'maxcgpi':maxcgpi}).fetchall()

    # print('cur_result',result,name,rollno,mincgpi,maxcgpi)

    print('Got result',diff())
    response_array['body'] = result
    return response_array

def get_single_result(rollno,sem=None):
    rollno = rollno.lower()
    conn = sqlite3.connect('nithResult.db')
    # rollnos = conn.execute('SELECT rollno FROM student WHERE rollno LIKE (?)',(rollno,)).fetchall()
    # for rollno,*_ in rollnos:
    response = {
        'rollno':rollno,
        'name':None,
        'head':None,
        'body':None,
        'summary_head': None,
        'summary_body': None
    }
    query_result = conn.execute('Select name from student where rollno=(?)',(rollno,)).fetchone()
    if query_result:
        response['name'] = query_result[0]
        # print(query_result,dir(query_result))
    if not sem:
        #If semester is not specified or sem==0, return result of all semesters
        cur = conn.execute('SELECT semester, code, title, credits, grade/credits as pointer \
            FROM result NATURAL JOIN course WHERE rollno=(?) ORDER BY semester ASC',(rollno,))
        cur2 = conn.execute('SELECT semester,sgpi,cgpi FROM summary where rollno=(?)',(rollno,))
    else:
        cur = conn.execute('SELECT semester, code, title, credits, grade/credits as pointer \
            FROM result NATURAL JOIN course WHERE rollno=(?) and semester=(?) ORDER BY semester ASC',(rollno,sem))
        cur2 = conn.execute('SELECT semester,sgpi,cgpi FROM summary \
            where rollno=(?) and semester=(?)',(rollno,sem))
        
    result = cur.fetchall()
    response['head'] = ('sem','code','title','credits','pointer')
    response['body'] = result

    result = cur2.fetchall()
    response['summary_head'] = ('sem','sgpi','cgpi')
    response['summary_body'] = result

    return response
