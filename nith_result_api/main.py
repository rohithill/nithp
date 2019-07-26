from flask import Blueprint

api = Blueprint('api',__name__)

@api.route('/')
def home():
    return "api reached"