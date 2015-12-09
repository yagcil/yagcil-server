import os
import mongoengine as me
from flask import Flask, jsonify
from flask.ext import restful
from flask.ext.cors import CORS

from yagcil.errorhandlers import AbstractError

app = Flask(__name__)
cors = CORS(app)
api = restful.Api(app)

if os.environ.get('DEBUG', 'true').lower() == 'false':
    app.config.from_object('yagcil.config.production')
    # Set up the database
    me.connect(host=app.config['MONGODB_URI']))
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


import yagcil.resources
