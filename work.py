from dotenv import load_dotenv
from flask import Flask, jsonify, request, abort
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from google.cloud import storage
import openai
import os
import uuid
import io

load_dotenv()

app = Flask(__name__)

def bucket_filename(user_id, filename):
    return str(user_id) + '/' + str(uuid.uuid4()) + '_' + secure_filename(filename)

def upload_file(bucket, user_id, file):
    filename = bucket_filename(user_id, file.filename)
    blob = bucket.blob(filename)
    blob.upload_from_string(file.read(), content_type=file.content_type, timeout=300)
    return blob.public_url

#@app.route('/work', methods=['POST'])
#@jwt_required()
def _create_work(request):
    user_id = get_jwt_identity()
    input_image = request.files['input']
    mask_image = request.files['mask']
    prompt = request.form['prompt']

    storage_client = storage.Client()
    bucket = storage_client.bucket(os.getenv('bucket_name'))

    if input_image and mask_image:
        input_public_url = upload_file(bucket, user_id, input_image)
        mask_public_url = upload_file(bucket, user_id, mask_image)
    else:
        abort(400)

    openai.api_key = os.getenv('OPENAI_KEY')
    response = openai.Image.create_edit(
        image=io.BufferedReader(input_image),
        mask=io.BufferedReader(mask_image),
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    work_info = {
        'input_url': input_public_url,
        'mask_url': mask_public_url,
        'output_url': response['data'][0]['url'],
    }

    return

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