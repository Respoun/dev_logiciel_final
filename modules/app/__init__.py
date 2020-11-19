''' flask app with mysql '''
import os
import json
import datetime
from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__,template_folder="dist")

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.environ.get('DB_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('DB_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.environ.get('DB_NAME')
app.config['MYSQL_DATABASE_HOST'] = os.environ.get('DB_HOST')
app.config['MYSQL_ROOT_PASSWORD'] = os.environ.get('DB_ROOT_PASSWORD')
mysql.init_app(app)

app.static_folder = 'static'
from app.controllers import *
