''' flask app with mongo '''
import os
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo


class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Flask(__name__,template_folder="dist")

app.config['MONGO_URI'] = os.environ.get('MONGO_DB_URI')
mongo = PyMongo(app)

app.static_folder = 'static'

app.json_encoder = JSONEncoder

from app.controllers import *
