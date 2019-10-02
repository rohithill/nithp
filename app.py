from flask import Flask, render_template, redirect, url_for, request
from nith_result.nith_result import result
from nith_result_api.main import api
from docs.main import docs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.register_blueprint(result,url_prefix='/result/')
app.register_blueprint(api,url_prefix='/api/')
app.register_blueprint(docs,url_prefix='/docs/')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return "Hi! I'm SimpleX."
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
if __name__ == '__main__':
    # To print all paths
    # print(app.url_map)
    app.run(debug=True)