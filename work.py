from dotenv import load_dotenv
from flask import Flask, jsonify, request, abort
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from pymongo import MongoClient
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
CORS(app)
app.config['JWT_SECRET_KEY'] = 'key'
jwt = JWTManager(app)

client = MongoClient('mongodb://loca:loca23!@127.0.0.1', 27017)

#@app.route('/work', methods=['POST'])
#def create_work():
#    return

#@app.route('/worklist', methods=['GET'])
#@jwt_required()
def _get_work_list():
    result = {}
    work_list = []
    db = client.userinfo
    collection = db['work']
    
    user_id = get_jwt_identity()
    print(user_id)
    
    keys = ['input_url', 'output_url', 'mask_url', 'prompt_text']
    
    # select all requests results of the user
    try:
        for doc in collection.find():
            try:
                if doc['user_id'] == user_id:
                    print("equal!!")
                    new_doc = {key: doc[key] for key in keys if key in doc}
                    print(new_doc)
                    work_list.append(new_doc)
                    print(work_list)
            except Exception as innere:
                print(innere)
                continue
    except Exception as e:
        print(e)
        result['success'] = 0

    result['work_list'] = work_list
    return result

#@app.route('/work/<int:work_id>', methods=['GET'])
#@jwt_required()
def _get_work(work_id):
    result = {}
    db = client.userinfo
    collection = db['work']
    
    id = get_jwt_identity()
    print(id)
    
    keys = ['input_url', 'output_url', 'mask_url', 'prompt_text']

    try:
        doc = collection.find_one({'_id': work_id})
        if doc['user_id'] == id:
            result['success'] = 1
            new_doc = {key: doc[key] for key in keys if key in doc}
            result['work'] = new_doc
        else:
            raise Exception("Invalid token")
    except Exception as e:
        result['success'] = 0
    return result

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)