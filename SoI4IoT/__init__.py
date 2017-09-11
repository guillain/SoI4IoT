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

# Load REST Full API server
from static.py.api import api
app.register_blueprint(api)

# Import SoI4IoT features
from static.py.login import login_app
app.register_blueprint(login_app)

from static.py.device import device_app
app.register_blueprint(device_app)

from static.py.user import user_app
app.register_blueprint(user_app)

from static.py.customer import customer_app
app.register_blueprint(customer_app)

from static.py.tracking import tracking_app
app.register_blueprint(tracking_app)

from static.py.dashboard import dashboard_app
app.register_blueprint(dashboard_app)

from static.py.tracker import tracker_app
app.register_blueprint(tracker_app)

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
