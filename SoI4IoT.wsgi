#!/usr/bin/python
# Target: apache swgi mapping
# Version: 0.1
# Date: 2017/01/04
# Mail: guillain@gmail.com
# Copyright 2017 GPL - Guillain

import os
import sys
import logging

sys.path.insert(0, '/var/www/SoI4IoT')
os.environ['FLASK_SETTING'] = '/var/www/SoI4IoT/conf/settings.cfg'

logging.basicConfig(stream=sys.stderr)

from SoI4IoT import app as application
