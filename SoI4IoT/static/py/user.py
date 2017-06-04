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
user_api = Blueprint('user_api', __name__)

# Conf app
api = Flask(__name__)
api.config.from_object(__name__)
api.config.from_envvar('FLASK_SETTING')

# User creation form -------------------------------------------
@user_api.route('/newUser', methods=['POST', 'GET'])
def newUser():
    wEvent('/newUser','request','Get new user','')
    return render_template('user.html')

# Save User ---------------------------------------------------
@user_api.route('/saveUser', methods=['POST'])
def newUserSub():
    try:
        sql  = "INSERT INTO user SET login = '" + request.form['login'] + "', "
        sql += "  firstname = '" + request.form['firstname'] + "', lastname = '" + request.form['lastname'] + "', "
        sql += "  email = '" + request.form['email'] + "', address = '" +request.form['address'] + "', "
        sql += "  admin = '" + request.form['admin'] + "', grp = '" + request.form['grp'] + "', "
        sql += "  password = '" + request.form['password'] + "', enterprise = '" + request.form['enterprise'] + "', "
        sql += "  mobile = '" + request.form['mobile'] + "' "
        sql += "ON DUPLICATE KEY UPDATE "
        sql += "  firstname = '" + request.form['firstname'] + "', lastname = '" + request.form['lastname'] + "', "
        sql += "  email = '" + request.form['email'] + "', address = '" +request.form['address'] + "', "
        sql += "  admin = '" + request.form['admin'] + "', grp = '" + request.form['grp'] + "', "
        sql += "  password = '" + request.form['password'] + "', enterprise = '" + request.form['enterprise'] + "', "
        sql += "  mobile = '" + request.form['mobile'] + "';"
        exeReq(sql)
        wEvent('/saveUser','exeReq','Save','OK')
        return 'Save OK'
    except Exception as e:
        wEvent('/saveUser','exeReq','Save','KO')
        return 'Save error'

# View User ---------------------------------------------------
@user_api.route('/viewUser', methods=['POST', 'GET'])
def viewUser():
    try:
        sql  = "SELECT uid, login, firstname, lastname, email, address, enterprise, grp, mobile, password, admin "
        sql += "FROM user WHERE login = '" + request.args['login'] + "';"
        view = exeReq(sql)
        wEvent('/viewUser','exeReq','Get','OK')
        return render_template('user.html', view = view[0])
    except Exception as e:
        wEvent('/viewUser','exeReq','Get','KO')
        return 'View error'

# List User --------------------------------------------------------
@user_api.route('/listUser', methods=['POST', 'GET'])
def listUser():
    try:
        list = exeReq("SELECT login, email, grp FROM user;")
        wEvent('/listUser','exeReq','Get','OK')
        return render_template('listUser.html', list = list)
    except Exception as e:
        wEvent('/listUser','exeReq','Get','KO')
        return 'List error'

# Map User ---------------------------------------------------------
@user_api.route('/mapUser', methods=['GET', 'POST'])
def mapUser():
    print 'hello'
    print request.args['login']
    try:
        gmap = exeReq("SELECT t.gps FROM tracking t, user u WHERE t.uid = u.uid AND u.login = '" + request.args['login'] + "';")
        wEvent('/mapUser','exeReq','Get','OK')
        return render_template('gmap.html', gmap = gmap)
    except Exception as e:
        wEvent('/mapUser','exeReq','Get','KO')
        return 'Map error'
