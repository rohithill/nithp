from flask import Flask, render_template, redirect, url_for
from nith_result.nith_result import result
from nith_result_api.main import api

app = Flask(__name__)

app.register_blueprint(result,url_prefix='/result/')
app.register_blueprint(api,url_prefix='/api/')

@app.route('/')
def home():
    return redirect(url_for('result.home'))
    # return render_template('index.html')

# To print all paths
# print(app.url_map)
@app.route('/about/')
def about():
    return "Hi! My name is SimpleX."

