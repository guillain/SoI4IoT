# Target: Device request mgt
# Version: 0.1
# Date: 2017/06/05
# Mail: guillain@gmail.com
# Copyright 2017 GPL - Guillain

from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template, jsonify, send_file
from werkzeug.utils import secure_filename
from tools import logger, exeReq, wEvent, getMaps, loginList

import re, os, sys, urllib

from flask import Blueprint
device_api = Blueprint('device_api', __name__)

# Conf app
api = Flask(__name__)
api.config.from_object(__name__)
api.config.from_envvar('FLASK_SETTING')

# Device creation form -------------------------------------------
@device_api.route('/newDevice', methods=['POST', 'GET'])
def newDevice():
    wEvent('/newDevice', 'request','Get new device','')
    return render_template('device.html', maps = '', loginList = loginList())

# Save device ------------------------------------------------
@device_api.route('/saveDevice', methods=['POST'])
def newDeviceSub():
    try:
        sql  = "INSERT INTO device SET name = '" + request.form['name'] + "', "
        sql += "  uid = (SELECT uid FROM user WHERE login = '" + request.form['login'] + "'), "
        sql += "  status = '" + request.form['status'] + "', description = '" + request.form['description'] + "' "
        sql += "ON DUPLICATE KEY UPDATE "
        sql += "  uid = (SELECT uid FROM user WHERE login = '" + request.form['login'] + "'), "
        sql += "  status = '" + request.form['status'] + "', description = '" + request.form['description'] + "';"
        exeReq(sql)
        wEvent('/saveDevice','exeReq','Save','OK')
        return 'Save OK'
    except Exception as e:
        wEvent('/saveDevice','exeReq','Save','KO')
        return 'Save error'

# View Device ---------------------------------------------------
@device_api.route('/viewDevice', methods=['POST', 'GET'])
def viewDevice():
    try:
        sql  = "SELECT d.did, u.login, d.name, d.description, d.status, d.lastupdate "
        sql += "FROM device d, user u "
        sql += "WHERE d.uid = u.uid AND d.name = '" + request.args['name'] + "';"
        view = exeReq(sql)
        wEvent('/viewDevice','exeReq','Get','OK')
        return render_template('device.html', view = view[0], maps = getMaps(), loginList = loginList())
    except Exception as e:
        wEvent('/viewDevice ','exeReq','Get','KO')
        return 'View error'

# List --------------------------------------------------------
@device_api.route('/listDevice', methods=['POST', 'GET'])
def listDevice():
    try:
        sql  = "SELECT d.name, u.login, d.status, d.lastupdate "
        sql += "FROM device d, user u "
        sql += "WHERE d.uid = u.uid AND d.status != 'deleted' AND u.grp != 'deleted';"
        list = exeReq(sql)
        wEvent('/listDevice','exeReq','Get list','OK')
        return render_template('listDevice.html', list = list, maps = getMaps())
    except Exception as e:
        wEvent('/listDevice','exeReq','Get list','KO')
        return 'List error'

# Delete Device ---------------------------------------------------
@device_api.route('/deleteDevice', methods=['POST', 'GET'])
def deleteDevice():
    try:
        sql  = "UPDATE device d, user u SET d.status = 'deleted' "
        sql += "WHERE d.uid = u.uid AND d.name = '" + request.args['name'] + "';"
        print sql
        view = exeReq(sql)
        wEvent('/deleteDevice','exeReq','Get','OK')
        return listDevice()
    except Exception as e:
        wEvent('/deleteDevice ','exeReq','Get','KO')
        return 'Delete error'

