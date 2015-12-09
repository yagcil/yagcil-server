"""
    API Server: production config

    NOTE: This setup is meant for OpenShift
"""
import os

SECRET_KEY = os.environ.get('SECRET_KEY')

SERVER_NAME = 'yagcil-api.herokuapp.com'
# Server root (just for API links generation)
SERVER_URL = 'http://{server}'.format(server=SERVER_NAME)

MONGODB_URI = os.environ.get('MONGOLAB_URI')
MONGODB_DB_NAME = os.environ.get('MONGODB_NAME')  # Database's name is the same as app's
MONGODB_DB_HOST = os.environ.get('MONGODB_HOST')
MONGODB_DB_PORT = os.environ.get('MONGODB_PORT')
MONGODB_DB_USERNAME = os.environ.get('MONGODB_USERNAME')
MONGODB_DB_PASSWORD = os.environ.get('MONGODB_PASSWORD')

YEARS = [2014, 2013, 2012, 2011]
