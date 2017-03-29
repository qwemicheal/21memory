from flask import Flask
from flask import jsonify
from flask import request
import sqlite3
import utils
from werkzeug.contrib.fixers import ProxyFix
app = Flask(__name__)
from logger import root
@app.route('/')
def hello_world():
    return 'Hello, World!'

dbmgr = utils.DatabaseManager("warehouse.db")


@app.route('/sign_in',methods=['POST','GET'])
def sign_in():
    if request.method == 'POST':
        root.info(request.get_json())
        root.info(request.data)
        root.info(request.headers)
        passwd = request.form["user[password]"]
        email = request.form["user[email]"]
        root.info("sign in  and get user email %s"%email)
        passwdhash=utils.get_hash(passwd)
        res=dbmgr.cur.execute("select * from user where user=?",(email,)).fetchone()
        root.info('db return %s '%(str(res)))
        if res!=None and res[1]==passwdhash:
            return jsonify({"email":"%s"%email,"authentication_token":passwdhash})
        else:
            abort(400)

@app.route('/get_content',methods=['POST','GET'])
def get_content():
    return jsonify({"result":[{"event_name": "3","time_left":"4"},{"event_name": "4","time_left":"5"}]})


@app.route('/sign_up',methods=['POST','GET'])
def sign_up():
    if request.method == 'POST':
        root.info(request.get_json())
        root.info(request.data)
        root.info(request.headers)
        passwd = request.form["user[password]"]
        email = request.form["user[email]"]
        root.info("sign up with user  %s"%email)
        if dbmgr.cur.execute("select * from user where user=?",(email,)).fetchone()==None:
            hashed_passwd=utils.get_hash(passwd)
            dbmgr.cur.execute("insert into user values (?,?)",(email,hashed_passwd,))
            root.info("after sign up with user  %s"%email)
            root.info(str(dbmgr.cur.execute("select * from user where user=?",(email,)).fetchone()))
            root.info(dbmgr.commit())
            return jsonify({"result":"sign up successfully ,log in use the credential created","email":"%s"%email,"authentication_token":str(hashed_passwd)})
        else:
            root.info("user  %s already exist"%email)
            return jsonify({"result":"user exist,you can log in directly","email":"%s"%email,"authentication_token":"0"})
    else:
        root.info("request method is get")
        root.info(request.headers)
        return jsonify({"result":"wrong method, use post to sign up"})


@app.route('/add',methods=['POST','GET'])
def add_record():
    if request.method == 'POST':
        root.info(request.form.getlist('new_record'))
        event = request.form["new_record"]
        root.info(request.headers)
        root.info("add record with name %s"%event)
        root.info("check user with header")
        user=utils.check_user_by_header(request.headers)
        if user != False:
            if dbmgr.cur.execute("select * from record where user=? and event=? and status=1",(user,event)).fetchone()==None:
                status=1
                days=
                dbmgr.cur.execute("insert into record values (?,?,?,?)",(user,event,days,status))
                root.info("after sign up with user  %s"%email)
                root.info(str(dbmgr.cur.execute("select * from user where user=?",(email,)).fetchone()))
                root.info(dbmgr.commit())
            else:
                return jsonify({"result":"event %s already exist"%event})
        else:
            return jsonify({"result":"user %s is not valid"%user})




@app.route('/erase',methods=['POST','GET'])
def erase_record():
    if request.method == 'POST':
        root.info(request.get_json())
        root.info(request.data)
        root.info(request.form.getlist('event'))
        event = request.form["event"]
        root.info("erase record with name %s"%event)
    else:
        event="empty"
    return jsonify({"result":"record %s removed"%event})

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
