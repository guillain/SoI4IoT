# Target: Request management
# Version: 0.1
# Date: 2017/02/05
# Mail: guillain@gmail.com
# Copyright 2017 GPL - Guillain

from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template, jsonify, send_file
from werkzeug.utils import secure_filename
from tools import logger, exeReq, wEvent

import re, os, sys, urllib

from flask import Blueprint
soi4ioT_api = Blueprint('soi4ioT_api', __name__)

# Conf app
api = Flask(__name__)
api.config.from_object(__name__)
api.config.from_envvar('FLASK_SETTING')

# Dashboard ---------------------------------------
@soi4ioT_api.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    try:
        dashboard = exeReq("SELECT gps FROM iot;")
        wEvent('/dashboard','exeReq','Get','OK')
        print str(dashboard)
        return render_template('dashboard.html', dashboard = dashboard)
    except Exception as e:
        wEvent('/dashboard','exeReq','Get','KO')
        return 'Dashboard error'

# IoT / human creation -------------------------------------------
@soi4ioT_api.route('/new', methods=['POST', 'GET'])
def new():
    wEvent('/new','request','Get new','')
    return render_template('new.html')

@soi4ioT_api.route('/newSub', methods=['POST'])
def newSub():
    try:
        sql  = "INSERT INTO iot SET "
        sql += "  login = '" + request.form['login'] +"', email = '" + request.form['email'] + "', "
        sql += "  firstname = '" + request.form['firstname'] + "', lastname = '" + request.form['lastname'] + "', "
        sql += "  admin = '" + request.form['admin'] + "', grp = '" + request.form['grp'] + "', "
        sql += "  password = '" + request.form['password'] +"', enterprise = '" + request.form['enterprise'] + "', "
        sql += "  gps = '" + request.form['gps'] + "', mobile = '" + request.form['mobile'] + "', "
        sql += "  ip = '" + request.form['ip'] + "', address = '" + request.form['address'] + "', "
        sql += "  webhook = '" + request.form['webhook'] + "', website = '" + request.form['website'] + "', "
        sql += "  deviceid = '" + request.form['deviceid'] + "', devicename = '" + request.form['devicename'] + "', "
        sql += "  devicestatus = '" + request.form['devicestatus'] + "', devicedescription = '" + request.form['devicedescription'] + "';"
    except Exception as e:
        wEvent('/newSub','arg','SQL request preparation','KO')
        return 'SQL request preparation issue'
    print sql
    try:
        iot = exeReq(sql)
        wEvent('/newSub','exeReq','Creation','OK')
        return 'Creation OK'
    except Exception as e:
        wEvent('/newSub','exeReq','Creation','KO')
        return 'Creation error'

# View ---------------------------------------------------
@soi4ioT_api.route('/view', methods=['POST', 'GET'])
def view():
    try:
        sql  = "SELECT login,firstname,lastname,password,email,enterprise,admin,grp,"
        sql += "  deviceid,devicename,devicedescription,devicestatus,deviceupdate,address,mobile,gps,ip,url,webhook,website "
        sql += "FROM iot WHERE login = '" + request.args['login'] + "';"
        view = exeReq(sql)
        wEvent('/view','exeReq','Get','OK')
        print str(view)
        return render_template('view.html', view = view[0])
    except Exception as e:
        wEvent('/view','exeReq','Get','KO')
        return 'View error'

# Update -------------------------------------------------
@soi4ioT_api.route('/update', methods=['POST'])
def update():
    try:
        sql  = "UPDATE iot SET "
        sql += "  firstname = '" + request.form['firstname'] + "', lastname = '" + request.form['lastname'] + "', "
        sql += "  admin = '" + request.form['admin'] + "', grp = '" + request.form['grp'] + "', "
        sql += "  password = '" + request.form['password'] +"', enterprise = '" + request.form['enterprise'] + "', "
        sql += "  gps = '" + request.form['gps'] + "', mobile = '" + request.form['mobile'] + "', "
        sql += "  ip = '" + request.form['ip'] + "', address = '" + request.form['address'] + "', "
        sql += "  webhook = '" + request.form['webhook'] + "', website = '" + request.form['website'] + "', "
        sql += "  deviceid = '" + request.form['deviceid'] + "', devicename = '" + request.form['devicename'] + "', " 
        sql += "  devicestatus = '" + request.form['devicestatus'] + "', devicedescription = '" + request.form['devicedescription'] + "' "
        sql += "WHERE login = '" + request.form['login'] + "';"
    except Exception as e:
        wEvent('/update','arg','SQL request preparation','KO')
        return 'SQL request preparation issue'

    try:
        user = exeReq(sql)
        wEvent('/update','exeReq','Update','OK')
        return 'Update OK'
    except Exception as e:
        wEvent('/update','exeReq','Update','KO')
        return 'Update error'

# List --------------------------------------------------------
@soi4ioT_api.route('/list', methods=['POST', 'GET'])
def list():
    try:
        list = exeReq("SELECT login,email,grp,devicename FROM iot;")
        wEvent('/list','exeReq','Get list','OK')
        return render_template('list.html', list = list)
    except Exception as e:
        wEvent('/list','exeReq','Get list','KO')
        return 'List error'

