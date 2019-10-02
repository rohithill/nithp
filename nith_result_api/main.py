from flask import Blueprint, jsonify
import sqlite3

api = Blueprint('api',__name__)

@api.route('/')
def home():
    return jsonify({"Status":1})

@api.route('/<string:rollno>/')
@api.route('/<string:rollno>/<int:sem>')
def getresult(rollno,sem=None):
    response = get_result(rollno,sem)
    return jsonify(response)

def get_result(rollno,sem=None):
    rollno = rollno.lower()
    response = {
        'rollno':None,
        'name':None,
        'fname': None,
        'head':None,
        'body':None
    }
    conn = sqlite3.connect('nithResult.db')
    response['name'],response['fname'] = conn.execute('Select name, father_name from student where rollno=(?)',(rollno,)).fetchone()
    if not sem:
        #If semester is not specified return result of all semesters
        cur = conn.execute('SELECT semester, code, title, credits, grade/credits as pointer \
            FROM result NATURAL JOIN course WHERE rollno=(?) ORDER BY semester ASC',(rollno,))
    else:
        cur = conn.execute('SELECT semester, code, title, credits, grade/credits as pointer \
            FROM result NATURAL JOIN course WHERE rollno=(?) and semester=(?) ORDER BY semester ASC',(rollno,sem))
    result = cur.fetchall()
    response['rollno'] = rollno
    response['head'] = ('semester','code','title','credits','pointer')
    response['body'] = result
    return response