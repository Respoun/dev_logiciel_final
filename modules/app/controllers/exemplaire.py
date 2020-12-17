''' controller and routes for exemplaire '''
import os
from flask import request, jsonify, render_template
from app import app, mongo
from pprint import pprint
import logger
import json

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/exemplaire', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def exemplaire():
    if request.method == 'GET':
        try:
            data = mongo.db.exemplaire.find()
            response = []
            for document in data:
                document['_id'] = str(document['_id'])
                livre = mongo.db.livre.find_one({"idlivre": document["idlivre"]},{'_id': False, 'titre': True, 'id_auteur': True, 'idemplacement': True})
                auteur = mongo.db.auteur.find_one({"id_auteur": livre["id_auteur"]}, {"_id": False})
                emplacement = mongo.db.emplacement.find_one({"idemplacement": livre["idemplacement"]},{'_id': False, 'nomemplacement': True})
                full_data = {**document, **livre, **auteur, **emplacement}
                response.append(full_data)
            return render_template("exemplaire.html", response=response), 200
        except Exception as e:
             return jsonify({'ok': False, 'message': str(e)}), 500
