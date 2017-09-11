#!flask/bin/python
# Target: api
# Version: 0.1
# Date: 2017/09/10
# Mail: guillain@gmail.com
# Copyright 2017 GPL - Guillain

from flask import Flask, jsonify, abort, request, make_response
from tools import logger, wEvent, exeJson

from flask import Blueprint
api = Blueprint('api', __name__)

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
        return [ 'tid', 'uid', 'did', 'ip', 'gps', 'url', 'website', 'webhook', 'address', 'timestamp', 'humidity', 'luminosity', 'temp_amb', 'temp_sensor' ]
    elif 'user' in ref:
        return [ 'uid', 'login', 'firstname', 'lastname', 'email', 'address', 'enterprise', 'grp', 'mobile', 'password', 'admin' ]
    else:
        wEvent('404','api',ref,'KO')
        abort(404)

# curl -i http://localhost:5000/api/v1.0/<item>/2
@api.route('/api/v1.0/<item>/<int:item_id>', methods=['GET'])
def get_item(item, item_id = None):
    try:
        fields = get_fields(item)

        sql  = "SELECT {} FROM {} WHERE {} = '{}';".format(','.join(fields), item, fields[0], item_id)
        print(sql)
        res = exeJson(sql, fields)
        wEvent('/api/v1.0/{}/{}'.format(item, item_id),'api','GET','OK')
        return jsonify({item: res})

    except Exception as e:
        wEvent('/api/v1.0/{}/{}'.format(item, item_id),'api','GET','KO')
        return jsonify({item: 'error'})

# curl -i http://localhost:5000/api/v1.0/<item>s
@api.route('/api/v1.0/<item>s', methods=['GET'])
def get_items(item):
    try:
        fields = get_fields(item)

        sql  = "SELECT {} FROM {};".format(','.join(fields), item, fields[0])
        print(sql)
        res = exeJson(sql, fields)
        wEvent('/api/v1.0/{}s'.format(item),'api','GET','OK')
        return jsonify({item: res})

    except Exception as e:
        wEvent('/api/v1.0/{}s'.format(item),'api','GET','KO')
        return jsonify({item: 'error'})


# curl -i -H "Content-Type: apilication/json" -X POST -d "{"""item""":"""tracking"""}" http://localhost:5000/api/v1.0/tracking
@api.route('/api/v1.0/<item>', methods=['POST'])
def create_item(item):
    #try:
        if not request.json or not 'item' in request.json:
            abort(400)

        item_id = 1 # ToDo: get back increment index after SQL injection

        wEvent('/api/v1.0/{}/{}'.format(item, item_id),'api','POST','OK')
        return jsonify({item: item_id}), 201

    #except Exception as e:
        wEvent('/api/v1.0/{}/{}'.format(item, item_id),'api','POST','KO')
        return jsonify({item: 'error'})

# curl -i -H "Content-Type: apilication/json" -X PUT -d '{"done":true}' http://localhost:5000/api/v1.0/<item>/2
@api.route('/api/v1.0/<item>/<int:item_id>', methods=['PUT'])
def update_item(item, item_id = None):
    #try:
        fields = get_fields(item)

        if len(fields) == 0:
            abort(404)
        if not request.json:
            abort(400)
        if 'item' in request.json and type(request.json['item']) != unicode:
            abort(400)
        if 'description' in request.json and type(request.json['description']) is not unicode:
            abort(400)
        if 'done' in request.json and type(request.json['done']) is not bool:
            abort(400)

        task[0]['title'] = request.json.get('title', task[0]['title'])
        task[0]['description'] = request.json.get('description', task[0]['description'])
        task[0]['done'] = request.json.get('done', task[0]['done'])

        wEvent('/api/v1.0/{}/{}'.format(item, item_id),'api','PUT','OK')
        return jsonify({item: task[0]})

    #except Exception as e:
        wEvent('/api/v1.0/{}/{}'.format(item, item_id),'api','PUT','KO')
        return jsonify({item: 'error'})

# curl -i -H "Content-Type: apilication/json" -X DELETE http://localhost:5000/api/v1.0/<item>/2
@api.route('/api/v1.0/<item>/<int:item_id>', methods=['DELETE'])
def delete_item(item, item_id = None):
    try:
        fields = get_fields(item)
        sql  = "UPDATE {} SET grp = 'deleted' WHERE {} = '{}';".format(item, fields[0], item_id)

        if item not in ('customer', 'user'):
            return jsonify({'result': False, 'Description': 'Not available in this item'})        

        exeJson(sql, fields)
        wEvent('/api/v1.0/{}/{}'.format(item, item_id),'api','DELETE','OK')
        return jsonify({'result': True}) 

    except Exception as e:
        wEvent('/api/v1.0/{}/{}'.format(item, item_id),'api','DELETE','KO')
        return jsonify({item: 'error'})

# curl -i http://localhost:5000/api/v1.0/<item>/3
@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
	

