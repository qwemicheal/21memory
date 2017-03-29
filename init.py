import utils
dbmgr = utils.DatabaseManager("warehouse.db")
dbmgr.cur.execute("drop table if exists record")
dbmgr.cur.execute("drop table if exists user")
dbmgr.cur.execute("create table user (user text,passhash text)")
dbmgr.cur.execute("create table record (user text,event text,days INTEGER,status INTEGER)")
dbmgr.commit()
