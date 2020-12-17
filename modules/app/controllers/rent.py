''' controller and routes for Rent '''
import os
from flask import request, jsonify, render_template
from app import app, mongo
from datetime import datetime
import logger
import json

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

@app.route('/rent', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def rent():
    if request.method == 'GET':
        now = datetime.now()
        try:
            data = mongo.db.emprunt.find_one(sort=[("idemprunt", -1)])["idemprunt"]
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            response = []
            response.append(data + 1)
            response.append(dt_string)
            return render_template("rent.html", response=response), 200
        except Exception as e:
             return jsonify({'ok': False, 'message': str(e)}), 500

    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            query = { "idexemplaire": data["idexemplaire"] }
            value = { "$set": { "disponibilite": "0" } }

            if data.get('idemprunt', None) is not None and data.get('dateemprunt', None) is not None and data.get('idutilisateur', None) is not None and data.get('idexemplaire', None) is not None:
                mongo.db.emprunt.insert_one(data)
                mongo.db.exemplaire.update_one(query,value)
                return render_template("index.html"), 200
        except Exception as e:
            return jsonify({'ok': False, 'message': 'Bad request parameters!', 'error': str(e)}), 400
