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

@app.route('/work', methods=['POST'])
@jwt_required()
def create_work():
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

    return

@app.route('/work', methods=['GET'])
def get_work_list():
    return

@app.route('/work/<int:work_id>', methods=['GET'])
def get_work(work_id):
    return