from flask import Blueprint, jsonify
import sqlite3

api = Blueprint('api',__name__)

@api.route('/')
def home():
    return jsonify({"Status":1})

@api.route('/<string:rollno>')
@api.route('/<string:rollno>/<int:sem>')
def getresult(rollno,sem=None):
    result = get_result(rollno,sem)
    return jsonify(result)

def get_result(rollno,sem=None):
    rollno = rollno.lower()
    conn = sqlite3.connect('nithResult.db')
    if not sem:
        #return result of all semesters
        cur = conn.execute('SELECT semester, code, title, credits, grade, grade/credits as pointer \
            FROM result NATURAL JOIN course WHERE rollno=(?) ORDER BY semester ASC',(rollno,))
    else:
        cur = conn.execute('SELECT semester, code, title, credits, grade, grade/credits as pointer \
            FROM result NATURAL JOIN course WHERE rollno=(?) and semester=(?) ORDER BY semester ASC',(rollno,sem))
    result = cur.fetchall()
    return result