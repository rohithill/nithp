from flask import Flask, render_template, redirect, url_for, request, g
from flask_cors import CORS
import connexion

from nith_result.nith_result import result
from docs.main import docs
from cache import cache
from gzipped import gzipped


connexionApp = connexion.App(__name__)
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

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return "Hi! I'm SimpleX."
    
if __name__ == '__main__':
    # print(app.url_map) # To print all paths
    # print(connexionApp.app.url_map)
    app.run(debug=True)
    
