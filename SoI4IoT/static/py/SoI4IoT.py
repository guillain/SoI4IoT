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
    wEvent('/dashboard','request','Get dashboard','')
    return render_template('dashboard.html')

# New -------------------------------------------
@soi4ioT_api.route('/new', methods=['POST', 'GET'])
def new():
    wEvent('/new','request','Get new','')
    return render_template('new.html')

@soi4ioT_api.route('/newSub', methods=['POST'])
def newSub():
    try:
        sql  = "INSERT INTO users (login,firstname,lastname,email,grp,mobile,gps,pw_hash,admin) VALUES"
        sql += "  ('" + request.form['login'] + "','" + request.form['firstname'] + "','" + request.form['lastname'] + "','"
        sql +=    request.form['email'] + "','" + request.form['grp'] + "','" + request.form['mobile'] + "','"
        sql +=    request.form['gps'] + "','" + request.form['pass'] + "','" + request.form['admin'] + "');"
    except Exception as e:
        wEvent('/newSub','arg','SQL request preparation','KO')
        return 'SQL request preparation issue'

    try:
        user = exeReq(sql)
        wEvent('/newSub','exeReq','User creation','OK')
        return 'User creation OK'
    except Exception as e:
        wEvent('/newSub','exeReq','User creation','KO')
        return 'User creation error'

# User ------------------------------------------
@soi4ioT_api.route('/user', methods=['POST', 'GET'])
def user():
    try:
        user = exeReq("SELECT login,firstname,lastname,email,mobile,GPS,admin,grp FROM users WHERE login = '"+request.args['login']+"';")
        wEvent('/user','exeReq','Get user','OK')
        return render_template('user.html', user = user[0])
    except Exception as e:
        wEvent('/user','exeReq','Get user','KO')
        return 'Get user error'

@soi4ioT_api.route('/userSub', methods=['POST','GET'])
def userSub():
    try:
        sql  = "UPDATE users SET "
        sql += "  firstname = '" + request.form['firstname'] + "', lastname = '" + request.form['lastname'] + "', "
        sql += "  admin = '" + request.form['admin'] + "', grp = '" + request.form['grp'] + "', "
        sql += "  gps = '" + request.form['gps'] + "', mobile = '" + request.form['mobile'] + "' "
        sql += "WHERE login = '" + request.form['login'] + "';"
    except Exception as e:
        wEvent('/userSub','arg','SQL request preparation','KO')
        return 'SQL request preparation issue'

    try:
        user = exeReq(sql)
        wEvent('/userSub','exeReq','User update','OK')
        return 'User update OK'
    except Exception as e:
        wEvent('/userSub','exeReq','User update','KO')
        return 'User update error'

# Users ------------------------------------------
@soi4ioT_api.route('/users', methods=['POST', 'GET'])
def users():
    try:
        users = exeReq("SELECT login,email,admin,grp FROM users;")
        wEvent('/users','exeReq','Get user list','OK')
        return render_template('users.html', users = users)
    except Exception as e:
        wEvent('/users','exeReq','Get user list','KO')
        return 'Get user list error'

@soi4ioT_api.route('/usersSub', methods=['POST'])
def usersSub():
    error = None
    return 'OK'

