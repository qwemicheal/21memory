import hashlib, binascii
import sqlite3
class DatabaseManager(object):
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def query(self, arg):
        self.cur.execute(arg)
        self.conn.commit()
        return self.cur

    def __del__(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

dbmgr = DatabaseManager("warehouse.db")

def get_hash(passwd):
    dk = hashlib.pbkdf2_hmac('sha256', b'%s'%passwd, b'wtfuicacnrqwe495', 100000)
    return binascii.hexlify(dk)

def check_user(user,token):
    res=dbmgr.cur.execute("select * from user where user=?",(user,)).fetchone()
    if res==None:
        return False
    else:
        if res[0]==user and res[1]==token:
            return user
        else:
            return False

def check_user_by_header(header):
    if "User" in header and "Token" in header:
        return check_user(header["User"],header["Token"])
    else:
        return False
