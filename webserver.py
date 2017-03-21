from flask import Flask
from flask import jsonify
from flask import request
from werkzeug.contrib.fixers import ProxyFix
app = Flask(__name__)
from logger import root
@app.route('/')
def hello_world():
    return 'Hello, World!'



@app.route('/test_json',methods=['POST'])
def test_json():
    print request.get_json()
    print request.data
    print request.form
    root.info("testing ")
    return jsonify('test jsoninfo')


@app.route('/get_test_json_return',methods=['POST'])
def return_json():
    return {"result":[{"row_name": "3"},{"row_name": "4"}]}

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
