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

# this route can be deleted, replaced by /search
# @result.route('/<string:rollno>/')
# def get_result(rollno):
#     rollno = rollno.lower()
#     result_array = api_result()
#     for result in result_array:
#         result['head'] = (*result['head'],'grade')
#         # calculate grade from pointer
#         for row in range(len(result['body'])):
#             result['body'][row] = (*result['body'][row],
#             pointer_to_grade[result['body'][row][result['head'].index('pointer')]])
#     # return "SDfasdf"
#     return render_template('nith_result/global_result.html',result_array=result_array)
@result.route('/student')
def result_student():
    rollno = request.args.get('rollno')
    result = get_single_result(rollno)
    # for result in result_array:
    result['head'] = (*result['head'],'grade')
        # calculate grade from pointer
    for row in range(len(result['body'])):
        result['body'][row] = (*result['body'][row],
        pointer_to_grade[result['body'][row][result['head'].index('pointer')]])
    # return "SDfasdf"
    # print(result)
    return render_template('nith_result/result_api.html',table=result)

@result.route('/search')
def search():
    rollno = request.args.get('roll')
    rollno = rollno.lower()

    import time
    st = time.perf_counter()
    response = api_result(rollno)    
    et = time.perf_counter()
    print("Time taken to process query: ", et - st)
    # print(response)
    # print(response.get('body'))
    return render_template('nith_result/search_result.html',table_head=response.get('head'),table_body=response.get('body'))