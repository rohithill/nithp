from flask import Blueprint, render_template, redirect

result = Blueprint('result',__name__,template_folder='templates',static_folder='static')

@result.route('/')
def home():
    return render_template('home.html')

from flask import Flask,request, jsonify, session, g, make_response
import json
import sqlite3
import urllib
from flask import url_for

@result.route('/<string:rollno>/')
def get_result(rollno):
    rollno = rollno.lower()
    from nith_result_api.main import get_result
    result = get_result(rollno)

    # print(result)
    return render_template('result.html',tables=result)
    return "GOOD"

@result.route('/handle_data',methods=['POST'])
def handle_data():
    roll_no = request.form['roll']
    return redirect(url_for('.get_result',rollno=roll_no))