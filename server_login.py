from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient
import warnings
from bson.objectid import ObjectId

warnings.simplefilter(action='ignore', category=FutureWarning) # FutureWarning 제거

client = MongoClient('mongodb://loca:loca23!@127.0.0.1', 27017)

def _login(req):
    req = request.json
    id = ObjectId(req['id'])
    password = req['password']
    success = False

    db = client.userinfo

    # Validate the id and password
    for d in db['users'].find():
        if d['_id'] == id and d['password'] == password:
            success = True
    if success:
        # If the credentials are valid, create and return the access token
        access_token = create_access_token(identity=id)
    else:
        return '', 401
    
    return jsonify(access_token=access_token)

def _register(req):
    id = req['id']
    password = req['password']
    
    db = client.userinfo
        
    # Insert into DB
    user_info = {
        '_id': ObjectId(id),
        'password': password,
    }
    
    try:
        db.users.insert_one(user_info)
    except Exception as e:
        print(e)
        return '', 401
    
    return {'success' : 1}