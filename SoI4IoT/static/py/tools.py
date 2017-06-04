# Target: tools for the app (db, wEvent, logger)
# Version: 0.1
# Date: 2017/01/18
# Mail: guillain@gmail.com
# Copyright 2017 GPL - Guillain

from flask import Flask, session, redirect, url_for, escape, request, flash
import MySQLdb

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTING')

# GPS SQL fct
def getMaps():
    # User arg as SQL condition
    try:
        login = " AND t.uid = u.uid AND u.login = '" + request.args['login'] + "'"
    except Exception as e:
        login = ' AND t.uid = u.uid'

    # Device arg as SQL condition
    try:
        name = " AND t.did = d.did AND d.name = '" + request.args['name'] + "'"
    except Exception as e:
        name = ' AND t.did = d.did'

    # Tracking arg as SQL condition
    try:
        tracking = " AND t.tid = '" + request.args['tracking'] + "'"
    except Exception as e:
        tracking = ''

    return exeReq("SELECT t.gps FROM tracking t, user u, device d WHERE 1" + login + name + tracking + ";")

# FUNCTIONs ---------------------------
# Log function (push in flash + log)
def logger(fct,msg):
  flash(msg)
  if app.config['DEBUG'] == 'True':
    print(str(fct+": "+msg))
  return

def wEvent(module, user, msg, status = None):
    logger(module,msg + ' ' + status)
    return exeReq("INSERT INTO events (module, user, msg, status) VALUES ('"+module+"', '"+user+"', '"+msg+"', '"+status+"');")

# DB functions
def connection():
    conn = MySQLdb.connect(
        host = app.config['MYSQL_HOST'],
        user = app.config['MYSQL_USER'],
        passwd = app.config['MYSQL_PASSWORD'],
        db = app.config['MYSQL_DB']
    )
    c = conn.cursor()
    return c, conn


def exeReq(req):
    error = None

    try:
        c, conn = connection()
    except Exception as e:
        logger('DB connection issue')
        return e

    try:
        c.execute(req)
        conn.commit()
    except Exception as e:
        logger('DB req execution issue')
        return e

    try:
        d = c.fetchall()
        c.close()
        return d
    except Exception as e:
        logger('DB fetch data issue')
        return e

