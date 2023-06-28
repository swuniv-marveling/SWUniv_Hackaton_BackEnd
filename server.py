from flask import Flask, render_template, jsonify, request

import multiprocessing as mp
import torch
import json
import random

app = Flask(__name__)

@app.route('/temp', methods=['POST'])
def temp():
    result = {}
    return ressult

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
