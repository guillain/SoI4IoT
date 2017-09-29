# Target: Device request mgt
# Version: 0.1
# Date: 2017/06/05
# Mail: guillain@gmail.com
# Copyright 2017 GPL - Guillain

from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template, jsonify, send_file
from flask_paginate import Pagination, get_page_parameter
from werkzeug.utils import secure_filename
from tools import logger, exeReq, wEvent, getMaps, loginList

import re, os, sys, urllib

from flask import Blueprint
device_app = Blueprint('device_app', __name__)

# Conf app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTING')

# Device creation form -------------------------------------------
@device_app.route('/html/v1.0/device/new', methods=['POST', 'GET'])
def newDevice():
    try:
        wEvent('/html/v1.0/device/new', 'request','Get new device','OK')
        return render_template('device.html', maps = '', loginList = loginList())
    except Exception as e:
        wEvent('/html/v1.0/device/new','request','Get new device','KO')
        return 'New error'

# Save device ------------------------------------------------
@device_app.route('/html/v1.0/device/save', methods=['POST'])
def newDeviceSub():
    try:
        sql  = "INSERT INTO device SET name = '" + request.form['name'] + "', "
        sql += "  uid = (SELECT uid FROM user WHERE login = '" + request.form['login'] + "'), "
        sql += "  status = '" + request.form['status'] + "', description = '" + request.form['description'] + "' "
        sql += "ON DUPLICATE KEY UPDATE "
        sql += "  uid = (SELECT uid FROM user WHERE login = '" + request.form['login'] + "'), "
        sql += "  status = '" + request.form['status'] + "', description = '" + request.form['description'] + "';"
        exeReq(sql)
        wEvent('/html/v1.0/device/save','exeReq','Save','OK')
        return 'Save OK'
    except Exception as e:
        wEvent('/html/v1.0/device/save','exeReq','Save','KO')
        return 'Save error'

# View Device ---------------------------------------------------
@device_app.route('/html/v1.0/device/view', methods=['POST', 'GET'])
def viewDevice():
    try:
        sql  = "SELECT d.did, u.login, d.name, d.description, d.status, d.lastupdate "
        sql += "FROM device d, user u "
        sql += "WHERE d.uid = u.uid AND d.name = '" + request.args['name'] + "';"
        view = exeReq(sql)
        wEvent('/html/v1.0/device/view','exeReq','Get','OK')
        return render_template('device.html', view = view[0], maps = getMaps(), loginList = loginList())
    except Exception as e:
        wEvent('/html/v1.0/device/view','exeReq','Get','KO')
        return 'View error'

# List --------------------------------------------------------
@device_app.route('/html/v1.0/device/list', methods=['POST', 'GET'])
def listDevice():
    try:
        sql_cont  = "FROM device d, user u "
        sql_cont += "WHERE d.uid = u.uid AND d.status != 'deleted' AND u.grp != 'deleted' "

        # Pagination
        search = False
        q = request.args.get('q')
        if q:
            search = True
        page = request.args.get(get_page_parameter(), type=int, default=1)
        per_page = 20
        startat = page * per_page
        if startat <= per_page:
            startat = 0
        count = exeReq("SELECT count(*) " + sql_cont)
        count = re.sub("[^0-9]", "","{}".format(count))
        pagination = Pagination(page=page, total=int(count), search=search, record_name='list', css_framework='foundation', per_page=per_page)

        sql  = "SELECT d.name, u.login, d.status, d.lastupdate "
        sql += "{} LIMIT {}, {};".format(sql_cont, startat, per_page)
        list = exeReq(sql)

        wEvent('/html/v1.0/device/list','exeReq','Get list','OK')
        return render_template('listDevice.html', list = list, maps = getMaps(), pagination=pagination)
    except Exception as e:
        wEvent('/html/v1.0/device/list','exeReq','Get list','KO')
        return 'List error'

# Export --------------------------------------------------------
@device_app.route('/html/v1.0/device/export', methods=['POST', 'GET'])
def exportDevice():
    try:
        sql  = "SELECT * "
        sql += "FROM device d, tracking t "
        sql += "WHERE d.did = t.did AND d.name = '" + request.args['name'] + "';"
        list = exeReq(sql)
        wEvent('/html/v1.0/device/export','exeReq','Get list','OK')
        return render_template('listTracking.html', list = list, maps = getMaps())

    except Exception as e:
        wEvent('/html/v1.0/device/export','exeReq','Get list','KO')
        return 'Export error'

# Delete Device ---------------------------------------------------
@device_app.route('/html/v1.0/device/delete', methods=['POST', 'GET'])
def deleteDevice():
    try:
        sql  = "UPDATE device d, user u SET d.status = 'deleted' "
        sql += "WHERE d.uid = u.uid AND d.name = '" + request.args['name'] + "';"
        print sql
        view = exeReq(sql)
        wEvent('/html/v1.0/device/delete','exeReq','Get','OK')
        return listDevice()
    except Exception as e:
        wEvent('/html/v1.0/device/delete','exeReq','Get','KO')
        return 'Delete error'

