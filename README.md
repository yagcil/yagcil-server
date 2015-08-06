# yagcil [![Build Status](https://travis-ci.org/yagcil/yagcil-server.svg)](https://travis-ci.org/yagcil/yagcil-server)
*Yet Another Google Code In Leaderboard - API server*

## Technologies
* Python
  * Flask (with Flask-RESTful)
* [MongoDB](http://www.mongodb-is-web-scale.com/)

## Setup
Make sure you have **Python** and **pip** installed.

The setup is easy as pie, creating **virtualenv** is recommended.
```
virtualenv yagcil-server
cd yagcil-server
source bin/activate
git clone http://github.com/yagcil/yagcil-server.git yagcil
cd yagcil
pip install -r requirements.txt
```

After all run the server with following command:

```
python runserver.py
```

### Database
Execute **update_db.py** script to update/setup the database.
#### Usage
* **--all**          Fetch all years
* **--active-year**  Fetch active year
* **--archive**      Fetch all years excluding the active year
* **-v, --verbose**  Be verbose
* **-d, --debug**    Enable debug information

The years are set in [Config](#Configuration), **YEARS=** key

## Configuration
In *yagcil-server* there are two types of configurations: 
**debug** and **production** (_yagcil.config.debug_ and _yagcil.config.production_). 
You can switch between them using the **DEBUG** environmental variable. 

By default **debug** config is loaded, set **DEBUG=False** to switch to production.

### OpenShift
```
rhc set-env DEBUG=False -a app
```

## Testing
*yagcil-server* uses [pytest](pytest.org) for testing, 
in order to run the tests correctly, **YAGCIL_TEST** environmental variable must be set to **True** (case insensitive)

To run the tests:

```
pip install -r requirements-test.txt
YAGCIL_TEST=True py.test
```

Testing requires a MongoDB instance running on **localhost:27015** (no auth)

## Note
This app is meant to be running on [OpenShift](http://openshift.com) (wsgi.py), 
but it can also run on [Heroku](http://heroku.com) (Procfile is needed) 
or any other cloud hosting with Python2.7 support (should [work on Py3.x too](http://flask.pocoo.org/docs/0.10/python3/))

## License
Copyright (C) 2015  Michał Proszek and Mateusz Maćkowski

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
