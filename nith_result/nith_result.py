from flask import Flask, Blueprint, render_template, redirect, request, url_for, jsonify
from nith_result_api import find_result as api_result,get_single_result, read as get_single_result, get_all_data
from cache import cache

import json
import operator
import time

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
@cache.cached(timeout=600,query_string=True)
def result_student():
    rollno = request.args.get('roll')
    result = get_single_result(rollno)
    return render_template('nith_result/single_student.html',result=result)

@result.route('/search')
@cache.cached(timeout=600,query_string=True)
def search():
    rollno = request.args.get('roll')
    rollno = rollno.lower()
    name = request.args.get('name')
    mincgpi = request.args.get('mincgpi')
    maxcgpi = request.args.get('maxcgpi')
    # next_cursor = request.args.get('next_cursor') or '0'

    st = time.perf_counter()
    results = get_all_data(name=name,roll=rollno,min_cgpi=mincgpi,max_cgpi=maxcgpi,limit=10000,sort_by_cgpi=True)
    et = time.perf_counter()
    print("Time taken to process Search query: ", et - st)

    return render_template('nith_result/search_result.html',results=results['data'])