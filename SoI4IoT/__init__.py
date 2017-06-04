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
from static.py.login import login_api
app.register_blueprint(login_api)

from static.py.device import device_api
app.register_blueprint(device_api)

from static.py.user import user_api
app.register_blueprint(user_api)

from static.py.tracking import tracking_api
app.register_blueprint(tracking_api)

from static.py.dashboard import dashboard_api
app.register_blueprint(dashboard_api)

# WEB mgt ----------------------------------------
@app.route('/')
def my_form():
  if 'login' in session:
    return render_template('welcome.html')
  return render_template("login.html")

# End of App --------------------------------------------------------------------------
if __name__ == '__main__':
    sess.init_app(app)
    app.debug = True
    app.run()
