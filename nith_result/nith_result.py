from flask import Flask, Blueprint, render_template, redirect, request, url_for, jsonify
from nith_result_api import find_result as api_result,get_single_result
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

@result.route('/student')
def result_student():
    rollno = request.args.get('rollno')
    print(request.args,request.values)
    result = get_single_result(rollno)

    # Add grade column as it's not returned by get_single_result
    result['head'] = (*result['head'],'grade')
    
    # calculate grade from pointer
    for row in range(len(result['body'])):
        result['body'][row] = (*result['body'][row],
        pointer_to_grade[result['body'][row][result['head'].index('pointer')]])
    
    return render_template('nith_result/result_student.html',table=result)

@result.route('/search')
def search():
    rollno = request.args.get('roll') or r'%'
    rollno = rollno.lower()
    name = request.args.get('name') or r'%'
    mincgpi = request.args.get('mincgpi') or None
    maxcgpi = request.args.get('maxcgpi') or None

    import time
    st = time.perf_counter()
    response = api_result(rollno,name,mincgpi,maxcgpi)    
    et = time.perf_counter()
    print("Time taken to process query: ", et - st)

    return render_template('nith_result/search_result.html',table_head=response.get('head'),table_body=response.get('body'))