''' controller and routes for emprunt '''
import os
from flask import request, jsonify, render_template
from app import app, mongo
from pprint import pprint
import logger
import json

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/emprunt', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def emprunt():
    if request.method == 'GET':
        try:
            data = mongo.db.emprunt.find({}, {'dateemprunt': False})
            response = []
            for document in data:
                document['_id'] = str(document['_id'])
                user = mongo.db.user.find_one({"idutilisateur": document["idutilisateur"]},{'_id': False, 'motdepasse': False})
                exemplaire = mongo.db.exemplaire.find_one({"idexemplaire": document["idexemplaire"]},{'_id': False})
                livre = mongo.db.livre.find_one({"idlivre": exemplaire["idlivre"]},{'_id': False, 'titre': True} )
                full_data = {**document, **user, **livre}
                response.append(full_data)
            return render_template("emprunt.html", response=response), 200
        except Exception as e:
             return jsonify({'ok': False, 'message': str(e)}), 500
