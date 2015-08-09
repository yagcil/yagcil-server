"""
    API Server: debug config
"""
DEBUG = True
SECRET_KEY = 'developement key'

MONGODB_DB_NAME = 'yagcil'

SERVER_NAME = 'localhost:5000'
# Server root (just for API links generation)
SERVER_URL = 'http://{server}'.format(server=SERVER_NAME)

# Years to be used in yagcil
YEARS = [2014, 2013, 2012]
