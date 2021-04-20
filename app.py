from flask import Flask, render_template, redirect, url_for, request, g
from flask_cors import CORS
import connexion
from swagger_ui_bundle import swagger_ui_3_path

from nith_result.nith_result import result
from docs.main import docs
from cache import cache
from gzipped import gzipped

import logging
log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

connexionApp = connexion.App(__name__,options={'swagger_path': swagger_ui_3_path,'swagger_url': 'doc'})
app = connexionApp.app

app.config['SECRET_KEY'] = 'you-will-never-guess'
# app.config['EXPLAIN_TEMPLATE_LOADING'] = True

CORS(app)
cache.init_app(app)

# combining various blueprints
app.register_blueprint(result,url_prefix='/result/')
app.register_blueprint(docs,url_prefix='/docs/')

# register swagger apis here
connexionApp.add_api('nith_result_api/swagger.yml')

app.finalize_request = gzipped(app.finalize_request)

@app.after_request
def add_header(response):
    response.cache_control.max_age = 300
    return response

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return "Hi! I'm SimpleX."
app2 = app
app = connexionApp
if __name__ == '__main__':
    # print(app.url_map) # To print all paths
    # print(connexionApp.app.url_map)
    app.run(debug=True)

