from flask import Flask, Blueprint, render_template, redirect, request, url_for
from nith_result_api.main import get_result as api_result

result = Blueprint('result',__name__,template_folder='templates',static_folder='static')

@result.route('/')
def home():
    return render_template('home.html')

@result.route('/<string:rollno>/')
def get_result(rollno):
    rollno = rollno.lower()
    result = api_result(rollno)
    return render_template('result_api.html',table=result)

@result.route('/handle_data',methods=['POST'])
def handle_data():
    roll_no = request.form['roll']
    return redirect(url_for('.get_result',rollno=roll_no))