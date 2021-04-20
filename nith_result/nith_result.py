from flask import Flask, Blueprint, render_template, redirect, request, url_for, jsonify

from nith_result_api import read as get_single_result, get_all_data
from utils import timer
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
    return render_template('nith_result/home.html',
        branches=['ARCHITECTURE',
            'CHEMICAL',
            'CIVIL',
            'CSE',
            'CSE_DUAL',
            'ECE',
            'ECE_DUAL',
            'ELECTRICAL',
            'MATERIAL',
            'MECHANICAL',
            'ENG_PHYSICS',
            'MAC'],
        years=['2015','2016','2017','2018','2019','2020'])

@result.route('/student')
@timer('WEBSITE read(roll)')
@cache.cached(timeout=600,query_string=True)
def result_student():
    rollno = request.args.get('roll')
    result = get_single_result(rollno)
    return render_template('nith_result/single_student.html',result=result)

@result.route('/search')
@timer('WEBSITE search')
@cache.cached(timeout=600,query_string=True)
def search():
    year = request.args.get('year')
    roll = None
    if year.isdecimal():
        if len(year) == 4:
            roll = year[-2:] + '%'

    data = {
        'roll' : request.args.get('roll') or roll,
        'name' : request.args.get('name'),
        'min_cgpi' : request.args.get('min_cgpi'),
        'max_cgpi' : request.args.get('max_cgpi'),
        'next_cursor' : request.args.get('next_cursor'),
        'branch' : request.args.get('branch'),
        'limit' : 10,
        'sort_by_cgpi' : 'true'
    }

    st = time.perf_counter()
    results = get_all_data(data,exceptional_limit=True)
    et = time.perf_counter()
    time_taken = et - st

    return render_template('nith_result/search_result.html',
        results=results['data'],
        next_cursor=results['pagination']['next_cursor'],
        time_taken=time_taken)
