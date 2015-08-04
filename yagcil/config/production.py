"""
    API Server: production config

    NOTE: This setup is meant for OpenShift
"""
import os

SECRET_KEY = os.environ.get('OPENSHIFT_SECRET_TOKEN')

MONGODB_DB_NAME = os.environ.get('OPENSHIFT_APP_NAME')  # Database's name is the same as app's
MONGODB_DB_HOST = os.environ.get('OPENSHIFT_MONGODB_DB_HOST')
MONGODB_DB_PORT = os.environ.get('OPENSHIFT_MONGODB_DB_PORT')
MONGODB_DB_USERNAME = os.environ.get('OPENSHIFT_MONGODB_DB_USERNAME')
MONGODB_DB_PASSWORD = os.environ.get('OPENSHIFT_MONGODB_DB_PASSWORD')

YEARS = [2014, 2013, 2012]
