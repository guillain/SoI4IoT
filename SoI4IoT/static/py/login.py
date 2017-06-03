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
login_api = Blueprint('login_api', __name__)

# Conf app
api = Flask(__name__)
api.config.from_object(__name__)
api.config.from_envvar('FLASK_SETTING')


# Record ------------------------------------------------------
@login_api.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if 'login' in session:
        return render_template('welcome.html')

    login = request.form['login']
    if not login:
        wEvent('/login','arg','Thanks to provide login','KO')
        return render_template('login.html')

    password = request.form['password']
    if not password:
        wEvent('/login','arg','Thanks to provide password','KO')
        return render_template('login.html')

    try:
        data = exeReq("SELECT grp, admin FROM user WHERE login='"+login+"' AND password=PASSWORD('"+password+"')")
    except Exception as e:
        wEvent('/login','','DB connection/request', 'KO')
        return render_template('login.html')

    try:
      if data is None or data[0][0] is None:
        wEvent('/login','','Wrong email or password','KO')
        return render_template('login.html')
    except Exception as e:
      wEvent('/login','','Wrong email or password','KO')
      return render_template('login.html')

    try:
        session['login'] = str(login)
        session['grp'] = str(data[0][0])
        session['admin'] = str(data[0][1])
        wEvent('/login',session['login'],"User "+session['login']+" logged",'OK')
        return render_template('welcome.html')
    except Exception as e:
        wEvent('/login','','Wrong email or password','KO')
        return render_template('login.html')

# Logout --------------------------------------------------
@login_api.route('/logout')
def logout():
  wEvent('/logout',session['login'],'You were logged out','OK')
  session.clear()
  return redirect('/')

