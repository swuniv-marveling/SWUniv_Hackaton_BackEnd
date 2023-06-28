from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient
import warnings
from bson.objectid import ObjectId

from server_login import _login, _register

warnings.simplefilter(action='ignore', category=FutureWarning) # FutureWarning 제거

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'key'
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    return _login(request.json)

@app.route('/register', methods=['POST'])
def register():
    return _register(request.json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
