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

# https://kb.sites.apiit.edu.my/knowledge-base/how-to-gzip-response-in-flask/
import gzip, functools
from io import BytesIO as IO
from flask import after_this_request, request

def gzipped(f):
    @functools.wraps(f)
    def view_func(*args, **kwargs):
        @after_this_request
        def zipper(response):
            accept_encoding = request.headers.get('Accept-Encoding', '')

            if 'gzip' not in accept_encoding.lower():
                return response

            response.direct_passthrough = False

            if (response.status_code < 200 or
                response.status_code >= 300 or
                'Content-Encoding' in response.headers):
                return response
            gzip_buffer = IO()
            gzip_file = gzip.GzipFile(mode='wb',
                                      fileobj=gzip_buffer)
            gzip_file.write(response.data)
            gzip_file.close()

            response.data = gzip_buffer.getvalue()
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Vary'] = 'Accept-Encoding'
            response.headers['Content-Length'] = len(response.data)

            return response

        return f(*args, **kwargs)
    return view_func

@result.route('/')
def home():
    return render_template('nith_result/home.html')

@result.route('/student')
def result_student():
    rollno = request.args.get('rollno')
    print(request.args,request.values)
    result = get_single_result(rollno)
    # print(result)

    # Add grade column as it's not returned by get_single_result
    result['head'] = (*result['head'],'grade')
    
    # calculate grade from pointer
    for row in range(len(result['body'])):
        result['body'][row] = (*result['body'][row],
        pointer_to_grade[result['body'][row][result['head'].index('pointer')]])
    
    # print(result)
    return render_template('nith_result/result_student.html',table=result)

@result.route('/search')
@gzipped
def search():
    rollno = request.args.get('roll')
    rollno = rollno.lower()
    name = request.args.get('name','%')
    mincgpi = request.args.get('mincgpi') or None
    maxcgpi = request.args.get('maxcgpi') or None
    print(mincgpi,maxcgpi,'here')
    print(request.values)
    import time
    st = time.perf_counter()
    response = api_result(rollno,name,mincgpi,maxcgpi)    
    et = time.perf_counter()
    print("Time taken to process query: ", et - st)
    # print(response)
    # print(response.get('body'))
    return render_template('nith_result/search_result.html',table_head=response.get('head'),table_body=response.get('body'))