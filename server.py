from flask import Flask, jsonify, request, make_response, render_template
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient
from flask_cors import CORS
import warnings
from bson.objectid import ObjectId

from server_login import _login, _register

warnings.simplefilter(action='ignore', category=FutureWarning) # FutureWarning 제거

app = Flask(__name__)
app.config['DEBUG'] = True
CORS(app)
app.config['JWT_SECRET_KEY'] = 'key'
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'OPTIONS': 
        return build_preflight_response()
    elif request.method == 'POST':
        return build_actual_response(_login(request.json))

def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def build_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/register', methods=['POST'])
def register():
    return _register(request.json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)

