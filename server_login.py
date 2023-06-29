from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient
import warnings
import json
from bson.objectid import ObjectId

warnings.simplefilter(action='ignore', category=FutureWarning) # FutureWarning 제거

client = MongoClient('mongodb://loca:loca23!@127.0.0.1', 27017)

def _login(req):
    req = request.json
    id = req['id']    #ObjectId(req['id'])
    password = req['password']
    success = False
    result = {}

    db = client.userinfo

    # Validate the id and password
    for d in db['users'].find():
        if d['_id'] == id and d['password'] == password:
            success = True
            break
    if success:
        # If the credentials are valid, create and return the access token
        access_token = create_access_token(identity=id)
        result['access_token'] = access_token
        result['success'] = 1
        try:
            result['name'] = d['name']
        except Exception as e:
            result['name'] = 'anonymous'
    else:
        result = { 'success' : 0 }
        make_response(result)
    
    result = make_response(result)
    return result


def _register(req):
    id = req['id']
    password = req['password']
    name = req['name']
    
    db = client.userinfo
        
    # Insert into DB
    user_info = {
        '_id': id,
        'password': password,
        'name': name,
    }
    
    try:
        db.users.insert_one(user_info)
    except Exception as e:
        print(e)
        return '', 401
    
    return {'success' : 1}