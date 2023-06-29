from dotenv import load_dotenv
from flask import Flask, jsonify, request, abort

load_dotenv()

app = Flask(__name__)

@app.route('/work', methods=['POST'])
def create_work():
    return

@app.route('/work', methods=['GET'])
def get_work_list():
    return

@app.route('/work/<int:work_id>', methods=['GET'])
def get_work(work_id):
    return