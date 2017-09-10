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
customer_app = Blueprint('customer_app', __name__)

# Conf app
api = Flask(__name__)
api.config.from_object(__name__)
api.config.from_envvar('FLASK_SETTING')

# Customer creation form -------------------------------------------
@customer_app.route('/newCustomer', methods=['POST', 'GET'])
def newCustomer():
    wEvent('/newCustomer','request','Get new user','')
    return render_template('customer.html', maps = '')

# Save Customer ---------------------------------------------------
@customer_app.route('/saveCustomer', methods=['POST'])
def newCustomerSub():
    try:
        sql  = "INSERT INTO user SET login = '" + request.form['login'] + "', "
        sql += "  firstname = '" + request.form['firstname'] + "', lastname = '" + request.form['lastname'] + "', "
        sql += "  email = '" + request.form['email'] + "', address = '" +request.form['address'] + "', "
        sql += "  admin = '0', grp = 'customer', "
        sql += "  password = '" + request.form['password'] + "', enterprise = '" + request.form['enterprise'] + "', "
        sql += "  mobile = '" + request.form['mobile'] + "' "
        sql += "ON DUPLICATE KEY UPDATE "
        sql += "  firstname = '" + request.form['firstname'] + "', lastname = '" + request.form['lastname'] + "', "
        sql += "  email = '" + request.form['email'] + "', address = '" +request.form['address'] + "', "
        sql += "  admin = '0', grp = 'customer', "
        sql += "  password = '" + request.form['password'] + "', enterprise = '" + request.form['enterprise'] + "', "
        sql += "  mobile = '" + request.form['mobile'] + "';"
        exeReq(sql)
        wEvent('/saveCustomer','exeReq','Save','OK')
        return 'Save OK'
    except Exception as e:
        wEvent('/saveCustomer','exeReq','Save','KO')
        return 'Save error'

# View Customer ---------------------------------------------------
@customer_app.route('/viewCustomer', methods=['POST', 'GET'])
def viewCustomer():
    try:
        sql  = "SELECT login, firstname, lastname, email, address, enterprise, mobile, password "
        sql += "FROM user WHERE login = '" + request.args['login'] + "' AND grp = 'customer';"
        view = exeReq(sql)
        wEvent('/viewCustomer','exeReq','Get','OK')
        return render_template('customer.html', view = view[0], maps = getMaps())
    except Exception as e:
        wEvent('/viewCustomer','exeReq','Get','KO')
        return 'View error'

# List Customer --------------------------------------------------------
@customer_app.route('/listCustomer', methods=['POST', 'GET'])
def listCustomer():
    try:
        list = exeReq("SELECT login, email, grp FROM user WHERE grp = 'customer';")
        wEvent('/listCustomer','exeReq','Get','OK')
        return render_template('listCustomer.html', list = list, maps = getMaps())
    except Exception as e:
        wEvent('/listCustomer','exeReq','Get','KO')
        return 'List error'

# Delete Customer ---------------------------------------------------
@customer_app.route('/deleteCustomer', methods=['POST', 'GET'])
def deleteCustomer():
    try:
        sql  = "UPDATE user SET grp = 'deleted' WHERE login = '" + request.args['login'] + "';"
        print sql
        exeReq(sql)
        wEvent('/deleteCustomer','exeReq','Get','OK')
        return listCustomer()
    except Exception as e:
        wEvent('/deleteCustomer ','exeReq','Get','KO')
        return 'Delete error'

