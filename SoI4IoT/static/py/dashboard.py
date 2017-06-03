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
dashboard_api = Blueprint('dashboard_api', __name__)

# Conf app
api = Flask(__name__)
api.config.from_object(__name__)
api.config.from_envvar('FLASK_SETTING')

# Dashboard ---------------------------------------
@dashboard_api.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    try:
        dashboard = exeReq("SELECT gps FROM tracking;")
        wEvent('/dashboard','exeReq','Get','OK')
        return render_template('gmap.html', gmap = dashboard)
    except Exception as e:
        wEvent('/dashboard','exeReq','Get','KO')
        return 'Dashboard error'

