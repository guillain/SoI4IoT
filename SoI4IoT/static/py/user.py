# Target: Request management
# Version: 0.1
# Date: 2017/02/05
# Mail: guillain@gmail.com
# Copyright 2017 GPL - Guillain

from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template, jsonify, send_file
from werkzeug.utils import secure_filename
from tools import logger, exeReq, wEvent, getMaps,loginList, nameList

import re, os, sys, urllib

from flask import Blueprint
user_app = Blueprint('user_app', __name__)

# Conf app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTING')

# User creation form -------------------------------------------
@user_app.route('/html/v1.0/user/new', methods=['POST', 'GET'])
def newUser():
    try:
        wEvent('/html/v1.0/user/new','request','Get new user','OK')
        return render_template('user.html', maps = '')
    except Exception as e:
        wEvent('/html/v1.0/user/new','request','Get new user','KO')
        return 'New error'

# Save User ---------------------------------------------------
@user_app.route('/html/v1.0/user/save', methods=['POST'])
def newUserSub():
    try:
        sql  = "INSERT INTO user SET login = '" + request.form['login'] + "', "
        sql += "  firstname = '" + request.form['firstname'] + "', lastname = '" + request.form['lastname'] + "', "
        sql += "  email = '" + request.form['email'] + "', address = '" +request.form['address'] + "', "
        sql += "  admin = '" + request.form['admin'] + "', grp = '" + request.form['grp'] + "', "
        sql += "  password = PASSWORD('" + request.form['password'] + "'), enterprise = '" + request.form['enterprise'] + "', "
        sql += "  mobile = '" + request.form['mobile'] + "' "
        sql += "ON DUPLICATE KEY UPDATE "
        sql += "  firstname = '" + request.form['firstname'] + "', lastname = '" + request.form['lastname'] + "', "
        sql += "  email = '" + request.form['email'] + "', address = '" +request.form['address'] + "', "
        sql += "  admin = '" + request.form['admin'] + "', grp = '" + request.form['grp'] + "', "
        sql += "  password = PASSWORD('" + request.form['password'] + "'), enterprise = '" + request.form['enterprise'] + "', "
        sql += "  mobile = '" + request.form['mobile'] + "';"
        exeReq(sql)
        wEvent('/html/v1.0/user/save','exeReq','Save','OK')
        return 'Save OK'
    except Exception as e:
        wEvent('/html/v1.0/user/save','exeReq','Save','KO')
        return 'Save error'

# View User ---------------------------------------------------
@user_app.route('/html/v1.0/user/view', methods=['POST', 'GET'])
def viewUser():
    try:
        sql  = "SELECT uid, login, firstname, lastname, email, address, enterprise, grp, mobile, '', admin "
        sql += "FROM user WHERE login = '" + request.args['login'] + "';"
        view = exeReq(sql)
        wEvent('/html/v1.0/user/view','exeReq','Get','OK')
        return render_template('user.html', view = view[0], maps = getMaps())
    except Exception as e:
        wEvent('/html/v1.0/user/view','exeReq','Get','KO')
        return 'View error'

# List User --------------------------------------------------------
@user_app.route('/html/v1.0/user/list', methods=['POST', 'GET'])
def listUser():
    try:
        list = exeReq("SELECT login, email, grp FROM user WHERE grp != 'deleted';")
        wEvent('/html/v1.0/user/list','exeReq','Get','OK')
        return render_template('listUser.html', list = list, maps = getMaps())
    except Exception as e:
        wEvent('/html/v1.0/user/list','exeReq','Get','KO')
        return 'List error'

# Delete User ---------------------------------------------------
@user_app.route('/html/v1.0/user/delete', methods=['POST', 'GET'])
def deleteUser():
    try:
        sql  = "UPDATE user SET grp = 'deleted' WHERE login = '" + request.args['login'] + "';"
        print sql
        exeReq(sql)
        wEvent('/html/v1.0/user/delete','exeReq','Get','OK')
        return listUser()
    except Exception as e:
        wEvent('/html/v1.0/user/delete','exeReq','Get','KO')
        return 'Delete error'

