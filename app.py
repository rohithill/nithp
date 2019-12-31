from flask import Flask, render_template, redirect, url_for, request, g
from nith_result.nith_result import result
from nith_result_api.main import api
from docs.main import docs
from cache import cache

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

cache.init_app(app)
# app.config['EXPLAIN_TEMPLATE_LOADING'] = True

app.register_blueprint(result,url_prefix='/result/')
app.register_blueprint(api,url_prefix='/api/')
app.register_blueprint(docs,url_prefix='/docs/')

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

app.finalize_request = gzipped(app.finalize_request)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    # import os
    # import multiprocessing
    # from pprint import pprint
    # pprint(os.getcwd())
    # pprint(os.environ)
    # pprint(multiprocessing.cpu_count())
    # pprint(os.cpu_count())
    # pprint(os.path.)
    return "Hi! I'm SimpleX."

if __name__ == '__main__':
    # print(app.url_map) # To print all paths
    app.run(debug=True)
