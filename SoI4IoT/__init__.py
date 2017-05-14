# Target: app init 
# Version: 0.1
# Date: 2017/01/04
# Mail: guillain@gmail.com
# Copyright 2017 GPL - Guillain

from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template, jsonify, flash, send_from_directory
from werkzeug.utils import secure_filename
from static.py.tools import logger, exeReq, wEvent
import re, os, sys, urllib

sys.path.append(os.path.dirname(__file__))

# Conf and create app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTING')

# Import SoI4IoT features
from static.py.SoI4IoT import soi4ioT_api
app.register_blueprint(soi4ioT_api)

# WEB mgt ----------------------------------------
@app.route('/')
def my_form():
  if 'login' in session:
    return render_template('new.html')
  return render_template("login.html")

# Login --------------------------------------------
@app.route('/login', methods=['POST'])
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
        data = exeReq("SELECT grp, admin FROM iot WHERE login='"+login+"' AND password=PASSWORD('"+password+"')")
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
@app.route('/logout')
def logout():
  wEvent('/logout',session['login'],'You were logged out','OK')
  session.clear()
  return redirect('/')

# End of App --------------------------------------------------------------------------
if __name__ == '__main__':
    sess.init_app(app)
    app.debug = True
    app.run()
