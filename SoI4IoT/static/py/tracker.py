# Target: Request management
# Version: 0.1
# Date: 2017/02/05
# Mail: guillain@gmail.com
# Copyright 2017 GPL - Guillain

from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template, jsonify, send_file
from werkzeug.utils import secure_filename
from tools import logger, exeReq, wEvent, getMaps

import re, os, sys, urllib

from flask import Blueprint
tracker_api = Blueprint('tracker_api', __name__)

# Conf app
api = Flask(__name__)
api.config.from_object(__name__)
api.config.from_envvar('FLASK_SETTING')

# Tracker ---------------------------------------
@tracker_api.route('/tracker', methods=['GET', 'POST'])
def tracker():
    try:
        wEvent('/tracker','exeReq','Get','OK')
        return render_template('tracker.html', maps = getMaps())
    except Exception as e:
        wEvent('/tracker','exeReq','Get','KO')
        return 'Tracker error'

@tracker_api.route('/saveTracker', methods=['POST'])
def saveTracker():
    #gps = request.form['latitude'] + ',' + request.form['longitude'];
    try:
        sql  = "INSERT INTO tracking SET "
        sql += "  uid = (SELECT uid FROM user WHERE login = '" + request.form['login'] + "'), "
        sql += "  did = (SELECT did FROM name WHERE name = '" + request.form['name'] + "'); "
        #sql += "  gps = '" + str(gps) + "';"
        print sql
        #exeReq(sql)
        wEvent('/saveTracker','exeReq','Get','OK')
        return 'Tracking updated'
    except Exception as e:
        wEvent('/saveTracker','exeReq','Get','KO')
        return 'Tracker error'

# Rec GPS
@tracker_api.route('/recGPS', methods=['POST'])
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

