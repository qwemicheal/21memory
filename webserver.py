from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)
from logger import root
@app.route('/')
def hello_world():
    return 'Hello, World!'



@app.route('/test_json',methods=['POST'])
def test_json():
    print request.get_json()
    root.info("testing ")
    return jsonify('test jsoninfo')
