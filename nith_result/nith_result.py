from flask import Blueprint, render_template

result = Blueprint('result',__name__,template_folder='templates',static_folder='static')

@result.route('/')
def home():
    return render_template('home.html')

from flask import Flask,request, jsonify, session, g, make_response
import json
import sqlite3

from flask import url_for

# @result.route('/<string:rollno>/')
# def get_result(rollno):
#     rollno = rollno.lower()
#     conn = sqlite3.connect('nithResult.db')
#     cur = conn.execute('SELECT semester, code, title, credits, grade, grade/credits as pointer FROM result NATURAL JOIN course WHERE rollno=(?) ORDER BY semester ASC',(rollno,))
#     result = cur.fetchall()
#     return jsonify(result)
@result.route('/<string:rollno>',defaults = {'sem':5})
# @result.route('/<string:rollno>/<int:sem>')
def get_sem_result(rollno,sem):
    rollno = rollno.lower()
    conn = sqlite3.connect('nithResult.db')
    cur = conn.execute('SELECT semester, code, title, credits, grade, grade/credits as pointer FROM result NATURAL JOIN course WHERE rollno=(?) and semester = (?) ORDER BY semester ASC',(rollno,sem))
    result = cur.fetchall()
    return jsonify(result)

    # if result is None:
        # return "<h1>Roll no not in database.</h1>"
    # else:
        # result = json.loads(result[0])
        # return render_template('result.html',tables=result)