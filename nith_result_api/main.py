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

init()   

def read_all():
    response = []
    for roll in results:
        r = results[roll]
        # print(r,type(r))
        temp = {
            "name": r["name"],
            "roll": r["roll"],
            "cgpi": r["cgpi"],
            "sgpi": r["sgpi"],
            "link": ('api/result/student/'+r["roll"])
        }
        response.append(temp)
    return response

def read(roll):
    if roll not in results:
        return "not found",404
    return results[roll]

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
