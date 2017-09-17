#!flask/bin/python
# Target: api
# Version: 0.1
# Date: 2017/09/10
# Mail: guillain@gmail.com
# Copyright 2017 GPL - Guillain

# Thanks to: 
# - https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

# Note:
# - item: table name (user, device, events, tracking)
# - field: field name comping from the concerned table


from flask import Flask, jsonify, abort, request, make_response
from tools import logger, wEvent, exeJson, exeReq
import urllib2, json, re

from flask import Blueprint
api = Blueprint('api', __name__)

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

# Conf app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTING')

# Check if item is included in the list
def get_fields(ref):
    if   'device' in ref:
        return [ 'did', 'uid', 'name', 'description', 'status', 'lastupdate' ]
    elif 'event' in ref:
        return [ 'eid', 'module', 'user', 'timestamp', 'msg', 'status' ]
    elif 'tracking' in ref:
        return [ 'tid', 'uid', 'did', 'ip', 'gps', 'url', 'website', 'webhook', 'address', 'timestamp', 'humidity', 'luminosity', 'temp_amb', 'temp_sensor', 'data' ]
    elif 'user' in ref:
        return [ 'uid', 'login', 'firstname', 'lastname', 'email', 'address', 'enterprise', 'grp', 'mobile', 'password', 'admin' ]
    elif 'iot' in ref:
        return [ 'tid', 'uid', 'did', 'humidity', 'luminosity', 'temp_amb', 'temp_sensor', 'data' ]
    else:
        wEvent('400','api',ref,'KO')
        abort(400)

# curl -u guillain:python -i http://localhost:5000/api/v1.0/<item>
@api.route('/api/v1.0/<item>', methods=['GET'])
@auth.login_required
def get_item(item):
    wEvent('/api/v1.0/{}'.format(item),'api','GET','OK')
    return jsonify({item: dict(zip(get_fields(item), get_fields(item)))})

# curl -u guillain:python -i http://localhost:5000/api/v1.0/<item>s
# curl -u guillain:python -i http://localhost:5000/api/v1.0/<item>/<int:item_id>
@api.route('/api/v1.0/<item>s', methods=['GET'])
@api.route('/api/v1.0/<item>/<int:item_id>', methods=['GET'])
@auth.login_required
def get_items(item, item_id = None):
    try:
        fields = get_fields(item)

        where = 1
        logpath = ''

        # /api/v1.0/<item>s  ==> with where close coming from JSON
        if request.json and item in request.json:
            logpath = '/api/v1.0/{}s'.format(item)
            where = ''
            for field in request.json[item]:
                where += "{} = '{}' AND ".format(field, request.json[item][field])
            where = sql[:-5]

        # '/api/v1.0/<item>/<int:item_id>'
        if item_id not in (None, ''):
            logpath = '/api/v1.0/{}/{}'.format(item,item_id)
            where = "{} = '{}'".format(fields[0], item_id)

        order = 'ASC'
        if 'order' in request.args:
            order = request.args['order']

        limit = 10
        if 'limit' in request.args:
            limit = request.args['limit']

        sql  = "SELECT {} FROM {} WHERE {} ORDER BY '{}' LIMIT {};".format(
            ','.join(fields), item, where, order, limit)

        res = exeJson(sql, fields)
        wEvent(logpath,'api','GET','OK')
        return jsonify({item: res})

    except Exception as e:
        wEvent(logpath,'api','GET','KO')
        abort(400)

# curl -u guillain:python -i -H "Content-Type: apilication/json" -X POST -d "{"""item""":"""tracking"""}" http://localhost:5000/api/v1.0/tracking
@api.route('/api/v1.0/<item>', methods=['POST'])
@auth.login_required
def create_item(item):
    try:
        if not request.json or not item in request.json:
            abort(400)

        if 'iot' in item:
            sql  = "INSERT INTO tracking SET "
            sql += "uid = '{}', ".format(request.json[item]['uid'])
            sql += "did = '{}', ".format(request.json[item]['did'])
            sql += "humidity = '{}', ".format(request.json[item]['hum'])
            sql += "luminosity = '{}', ".format(request.json[item]['lum'])
            sql += "temp_amb = '{}', ".format(request.json[item]['tam'])
            sql += "temp_sensor = '{}', ".format(request.json[item]['tse'])
            sql += 'data = "{}";'.format(request.json)
            item = 'tracking'
        else:
            fields = get_fields(item)

            sql = 'INSERT INTO {} SET '.format(item)
            for field in request.json[item]:
                sql += '{} = "{}", '.format(field, request.json[item][field])
            sql = sql[:-2] + ';'

        exeReq(sql)

        res = exeReq("SELECT COUNT(*) FROM {};".format(item))
        item_id = re.sub("[^0-9]", "","{}".format(res))

        wEvent('/api/v1.0/{}/{}'.format(item, item_id),'api','POST','OK')
        return jsonify({item: item_id}), 201

    except Exception as e:
        wEvent('/api/v1.0/{}'.format(item),'api','POST','KO')
        abort(400)

# curl -u guillain:python -i -H "Content-Type: apilication/json" -X PUT -d '{"done":true}' http://localhost:5000/api/v1.0/<item>/2
@api.route('/api/v1.0/<item>/<int:item_id>', methods=['PUT'])
@auth.login_required
def update_item(item, item_id):
    try:
        fields = get_fields(item)

        if not request.json and item not in request.json:
            abort(400)

        sql = 'UPDATE {} SET '.format(item)
        for field in request.json[item]:
            sql += "{} = '{}', ".format(field, request.json[item][field])
        sql = sql[:-2] + " WHERE {} = '{}';".format(fields[0], item_id)

        exeReq(sql)

        wEvent('/api/v1.0/{}/{}'.format(item, item_id),'api','PUT','OK')
        return jsonify({item: task[0]})

    except Exception as e:
        wEvent('/api/v1.0/{}/{}'.format(item, item_id),'api','PUT','KO')
        abort(400)

# curl -u guillain:python -i -H "Content-Type: apilication/json" -X DELETE http://localhost:5000/api/v1.0/<item>/2
@api.route('/api/v1.0/<item>/<int:item_id>', methods=['DELETE'])
@auth.login_required
def delete_item(item, item_id = None):
    if item not in ('customer', 'user'):
        return jsonify({'result': False, 'Description': 'Not available in this item'})

    try:
        fields = get_fields(item)
        sql  = "UPDATE {} SET grp = 'deleted' WHERE {} = '{}';".format(item, fields[0], item_id)

        exeJson(sql, fields)
        wEvent('/api/v1.0/{}/{}'.format(item, item_id),'api','DELETE','OK')
        return jsonify({'result': True}) 

    except Exception as e:
        wEvent('/api/v1.0/{}/{}'.format(item, item_id),'api','DELETE','KO')
        abort(400)

# curl -u guillain:python -i http://localhost:5000/api/v1.0/<item>/99999999999
@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), error)

# curl-u ko:ko -i http://localhost:5000/api/v1.0/<item>/1
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

# Authentification functions
@auth.get_password
def get_password(username):
    if username == app.config['API_USER']:
        return app.config['API_TOKEN']
    return None

def get_auth_token():
    req=urllib2.Request("https://xforce-api.mybluemix.net/auth/anonymousToken")
    response=urllib2.urlopen(req)
    html=response.read()
    json_obj=json.loads(html)
    token_string=json_obj["token"].encode("ascii","ignore")
    return token_string

def get_response_json_object(url, auth_token):
    auth_token=get_auth_token()
    req=urllib2.Request(url, None, {"Authorization": "Bearer %s" %auth_token})
    response=urllib2.urlopen(req)
    html=response.read()
    json_obj=json.loads(html)
    return json_obj

