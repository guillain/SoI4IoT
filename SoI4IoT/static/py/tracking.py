# Target: Request management
# Version: 0.1
# Date: 2017/02/05
# Mail: guillain@gmail.com
# Copyright 2017 GPL - Guillain

from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template, jsonify, send_file
from werkzeug.utils import secure_filename
from tools import logger, exeReq, wEvent, getMaps, loginList, nameList

import re, os, sys, urllib

from flask import Blueprint
tracking_app = Blueprint('tracking_app', __name__)

# Conf app
api = Flask(__name__)
api.config.from_object(__name__)
api.config.from_envvar('FLASK_SETTING')

# Tracking creation form -------------------------------------------
@tracking_app.route('/newTracking', methods=['POST', 'GET'])
def newTracking():
    wEvent('/newTracking','request','Get new tracking','')
    return render_template('tracking.html', maps = '', loginList = loginList(), nameList = nameList())

# Save Tracking ---------------------------------------------------
@tracking_app.route('/saveTracking', methods=['POST'])
def saveTracking():
    try:
        sql  = "INSERT INTO tracking SET tid = '" + request.form['tracking'] + "', "
        sql += "  uid = (SELECT uid FROM user WHERE login = '" + request.form['login'] + "'), "
        sql += "  did = (SELECT did FROM device WHERE name = '" + request.form['name'] + "'), "
        sql += "  gps = '" + request.form['gps'] + "', url = '" +request.form['url'] + "', "
        sql += "  website = '" + request.form['website'] + "', webhook = '" + request.form['webhook'] + "', "
        sql += "  address = '" + request.form['address'] + "', ip = '" +request.form['ip'] + "', "
        sql += "  humidity = '" + request.form['humidity'] + "', luminosity = '" + request.form['luminosity'] + "', "
        sql += "  temp_amb = '" + request.form['temp_amb'] + "', temp_sensor = '" +request.form['temp_sensor'] + "' "
        sql += "ON DUPLICATE KEY UPDATE "
        sql += "  uid = (SELECT uid FROM user WHERE login = '" + request.form['login'] + "'), "
        sql += "  did = (SELECT did FROM device WHERE name = '" + request.form['name'] + "'), "
        sql += "  gps = '" + request.form['gps'] + "', url = '" +request.form['url'] + "', "
        sql += "  website = '" + request.form['website'] + "', webhook = '" + request.form['webhook'] + "', "
        sql += "  address = '" + request.form['address'] + "', ip = '" +request.form['ip'] + "', "
        sql += "  humidity = '" + request.form['humidity'] + "', luminosity = '" + request.form['luminosity'] + "', "
        sql += "  temp_amb = '" + request.form['temp_amb'] + "', temp_sensor = '" +request.form['temp_sensor'] + "';"
        exeReq(sql)
        wEvent('/saveTracking','exeReq','Save','OK')
        return 'Save OK'
    except Exception as e:
        wEvent('/saveTracking','exeReq','Save','KO')
        return 'Save error'

# View Tracking ---------------------------------------------------
@tracking_app.route('/viewTracking', methods=['POST', 'GET'])
def viewTracking():
    try:
        sql  = "SELECT t.tid, u.login, d.name, t.ip, t.gps, t.url, t.website, t.webhook, t.address, t.timestamp, t.humidity, t.luminosity, t.temp_amb, t.temp_sensor "
        sql += "FROM tracking t, user u, device d "
        sql += "WHERE u.uid = t.uid AND t.did = d.did AND t.tid = '" + request.args['tracking'] + "';"
        view = exeReq(sql)
        wEvent('/viewTracking','exeReq','Get','OK')
        return render_template('tracking.html', view = view[0], maps = getMaps(), loginList = loginList(), nameList = nameList())
    except Exception as e:
        wEvent('/viewTracking','exeReq','Get','KO')
        return 'View error'

# List Tracking --------------------------------------------------------
@tracking_app.route('/listTracking', methods=['POST', 'GET'])
def listTracking():
    try:
        sql  = "SELECT t.tid, u.login, d.name, t.timestamp, CONCAT_WS(t.ip, t.gps, t.url, t.website, t.webhook, t.address, t.humidity, t.luminosity, t.temp_amb, t.temp_sensor) "
        sql += "FROM tracking t, user u, device d "
        sql += "WHERE t.uid = u.uid AND t.did = d.did AND u.grp != 'deleted' AND d.status != 'deleted';"
        list = exeReq(sql)
        wEvent('/listTracking','exeReq','Get list','OK')
        return render_template('listTracking.html', list = list, maps = getMaps())
    except Exception as e:
        wEvent('/listTracking','exeReq','Get list','KO')
        return 'List error'
