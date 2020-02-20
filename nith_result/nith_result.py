from flask import Flask, Blueprint, render_template, redirect, request, url_for, jsonify
from nith_result_api import find_result as api_result,get_single_result
import json
from cache import cache

result = Blueprint('result',__name__,template_folder='templates',static_folder='static')

pointer_to_grade = {
    10: 'A',
    9 : 'AB',
    8 : 'B',
    7 : 'BC',
    6 : 'C',
    5 : 'CD', #rollno 17635
    4 : 'D',
    0 : 'F'
}


@result.route('/')
def home():
    return render_template('nith_result/home.html')

@result.route('/student')
def result_student():
    rollno = request.args.get('rollno')
    # print(request.args,request.values)
    result = get_single_result(rollno)

    # Add grade column as it's not returned by get_single_result
    result['head'] = (*result['head'],'grade')
    
    # calculate grade from pointer
    for row in range(len(result['body'])):
        result['body'][row] = (*result['body'][row],
        pointer_to_grade[result['body'][row][result['head'].index('pointer')]])
    table_summary = {'body' : [(1,8,8)]}
    return render_template('nith_result/result_student.html',table=result,table_summary=table_summary)

import operator
@result.route('/search')
@cache.cached(timeout=600,query_string=True)
def search():
    rollno = request.args.get('roll')
    rollno = rollno.lower()
    name = request.args.get('name')
    mincgpi = request.args.get('mincgpi')
    maxcgpi = request.args.get('maxcgpi')

    # print(mincgpi,maxcgpi,name,rollno,'here')
    import time
    st = time.perf_counter()
    response = api_result(rollno,name,mincgpi,maxcgpi)    
    et = time.perf_counter()
    print("Time taken to process query: ", et - st)
    # print(response)
    table_head = response.get('head')
    table_body = response.get('body')

    table_body.sort(key=operator.itemgetter(table_head.index('cgpi')),reverse=True)

    return render_template('nith_result/search_result.html',table_head=table_head,table_body=table_body)