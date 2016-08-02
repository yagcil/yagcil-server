import os
import mongoengine as me
from flask import Flask, jsonify, request
from flask.ext import restful
from flask.ext.cors import CORS

from yagcil.errorhandlers import AbstractError

app = Flask(__name__)
cors = CORS(app)
api = restful.Api(app)

if os.environ.get('DEBUG', 'true').lower() == 'false':
    app.config.from_object('yagcil.config.production')
    # Set up the database
    me.connect(
        app.config['MONGODB_DB_NAME'],
        host=app.config['MONGODB_DB_HOST'],
        port=app.config['MONGODB_DB_PORT'],
        username=app.config['MONGODB_DB_USERNAME'],
        password=app.config['MONGODB_DB_PASSWORD']
    )
else:
    app.config.from_object('yagcil.config.debug')
    # If testing is on, let connect to the database later
    if os.environ.get('YAGCIL_TEST', 'false').lower() == 'false':
        me.connect(app.config['MONGODB_DB_NAME'])


@app.errorhandler(AbstractError)
def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code

    return response


payu_data = {}

@app.route('/payu_online'):
def payu_online():
    payu_data = request.args
    return ""
    
@app.route('/payu'):
    return payu_data

import yagcil.resources
