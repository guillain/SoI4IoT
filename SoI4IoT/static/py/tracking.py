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
tracking_api = Blueprint('tracking_api', __name__)

# Conf app
api = Flask(__name__)
api.config.from_object(__name__)
api.config.from_envvar('FLASK_SETTING')


# Record ------------------------------------------------------
@tracking_api.route('/recGPS', methods=['POST', 'GET'])
def recGPS():
    gps = request.form['latitude'] + ',' + request.form['longitude'];

    # Check if webbrowser device is recorded, if not add it
    try:
        sql  = "INSERT INTO device SET uid = (SELECT uid FROM user WHERE login = '" + request.form['login'] + "'), "
        sql += "  name = '" + request.user_agent.browser + "', status = 'ok', description = '" + request.user_agent.string + "' "
        sql += "ON DUPLICATE KEY UPDATE status = 'ok';"
        exeReq(sql)

        sql  = "SELECT did FROM device "
        sql += "WHERE name = '" + request.user_agent.browser + "' AND status = 'ok' AND description = '" + request.user_agent.string + "' "
        sql += "ORDER BY did DESC LIMIT 1;"
        did = exeReq(sql)
        wEvent('/recGPS','exeReq','Add or update web device','OK')
    except Exception as e:
        wEvent('/recGPS','exeReq','Add or update web device','KO')
        return 'Add or update web device error'

    # Add new localisation
    try:
        sql  = "INSERT INTO tracking SET "
        sql += "  uid = (SELECT uid FROM user WHERE login = '" + request.form['login'] + "'), "
        sql += "  did = '" + str(did[0][0]) + "', gps = '" + str(gps) + "';"
        exeReq(sql)
        wEvent('/recGPS','exeReq','GPS record','OK')
        return 'GPS record OK'
    except Exception as e:
        wEvent('/recGPS','exeReq','GPS record','KO')
        return 'GPS record error'

# Tracking creation form -------------------------------------------
@tracking_api.route('/newTracking', methods=['POST', 'GET'])
def newTracking():
    wEvent('/newTracking','request','Get new tracking','')
    return render_template('tracking.html')

# Save Tracking ---------------------------------------------------
@tracking_api.route('/saveTracking', methods=['POST'])
def saveTracking():
    try:
        sql  = "INSERT INTO tracking SET "
        sql += "  uid = (SELECT uid FROM user WHERE login = '" + request.form['login'] + "'), "
        sql += "  did = (SELECT did FROM device WHERE name = '" + request.form['name'] + "'), "
        sql += "  gps = '" + request.form['gps'] + "', url = '" +request.form['url'] + "', "
        sql += "  website = '" + request.form['website'] + "', webhook = '" + request.form['webhook'] + "', "
        sql += "  address = '" + request.form['address'] + "', ip = '" +request.form['ip'] + "' "
        sql += "ON DUPLICATE KEY UPDATE "
        sql += "  uid = (SELECT uid FROM user WHERE login = '" + request.form['login'] + "'), "
        sql += "  did = (SELECT did FROM device WHERE name = '" + request.form['name'] + "'), "
        sql += "  gps = '" + request.form['gps'] + "', url = '" +request.form['url'] + "', "
        sql += "  website = '" + request.form['website'] + "', webhook = '" + request.form['webhook'] + "', "
        sql += "  address = '" + request.form['address'] + "', ip = '" +request.form['ip'] + "';"
        print sql
        exeReq(sql)
        wEvent('/saveTracking','exeReq','Save','OK')
        return 'Save OK'
    except Exception as e:
        wEvent('/saveTracking','exeReq','Save','KO')
        return 'Save error'

# View Tracking ---------------------------------------------------
@tracking_api.route('/viewTracking', methods=['POST', 'GET'])
def viewTracking():
    try:
        sql  = "SELECT t.tid, u.login, d.name, t.ip, t.gps, t.url, t.website, t.webhook, t.address, t.timestamp "
        sql += "FROM tracking t, user u, device d "
        sql += "WHERE u.uid = t.uid AND t.tid = '" + request.args['tracking'] + "';"
        view = exeReq(sql)
        wEvent('/viewTracking','exeReq','Get','OK')
        return render_template('tracking.html', view = view[0])
    except Exception as e:
        wEvent('/viewTracking','exeReq','Get','KO')
        return 'View error'

# List Tracking --------------------------------------------------------
@tracking_api.route('/listTracking', methods=['POST', 'GET'])
def listTracking():
    try:
        sql  = "SELECT t.tid, u.login, d.name, t.timestamp, CONCAT_WS(t.ip, t.gps, t.url, t.website, t.webhook, t.address) "
        sql += "FROM tracking t, user u, device d "
        sql += "WHERE t.uid = u.uid AND t.did = d.did;"
        list = exeReq(sql)
        wEvent('/listTracking','exeReq','Get list','OK')
        return render_template('listTracking.html', list = list)
    except Exception as e:
        wEvent('/listTracking','exeReq','Get list','KO')
        return 'List error'

# Map ----------------------------------------------------------
@tracking_api.route('/mapTracking', methods=['GET', 'POST'])
def mapTracking():
    try:
        data = exeReq("SELECT gps FROM tracking")
        wEvent('/mapTracking','exeReq','Get','OK')
        return render_template('gmap.html', gmap = data)
    except Exception as e:
        wEvent('/mapTracking','exeReq','Get','KO')
        return 'Map error'

