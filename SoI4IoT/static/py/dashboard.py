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
dashboard_app = Blueprint('dashboard_app', __name__)

# Conf app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTING')

# Dashboard ---------------------------------------
@dashboard_app.route('/html/v1.0/dashboard', methods=['GET', 'POST'])
def dashboard():
    try:
        wEvent('/html/v1.0/dashboard','exeReq','Get','OK')
        return render_template('dashboard.html', maps = getMaps())
    except Exception as e:
        wEvent('/html/v1.0/dashboard','exeReq','Get','KO')
        return 'Dashboard error'

