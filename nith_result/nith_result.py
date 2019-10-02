from flask import Flask, Blueprint, render_template, redirect, request, url_for, jsonify
from nith_result_api.main import get_result as api_result
import json

result = Blueprint('result',__name__,template_folder='templates',static_folder='static')

pointer_to_grade = {
    10: 'A',
    9 : 'AB',
    8 : 'B',
    7 : 'BC',
    6 : 'C',
    4 : 'D',
    0 : 'F'
}

@result.route('/')
def home():
    return render_template('nith_result/home.html')

@result.route('/<string:rollno>/')
def get_result(rollno):
    rollno = rollno.lower()
    result = api_result(rollno)
    result['head'] = (*result['head'],'grade')
    # calculate grade from pointer
    for row in range(len(result['body'])):
        result['body'][row] = (*result['body'][row],
        pointer_to_grade[result['body'][row][result['head'].index('pointer')]])
    return render_template('nith_result/result_api.html',table=result)

@result.route('/handle_data',methods=['POST'])
def handle_data():
    roll_no = request.form['roll']
    return redirect(url_for('.get_result',rollno=roll_no))