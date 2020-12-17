''' controller and routes for livre '''
import os
from flask import request, jsonify, render_template
from app import app, mongo
from pprint import pprint
import logger
import json

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/livre', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def livre():
    if request.method == 'GET':
        try:
            data = mongo.db.livre.find()
            response = []
            for document in data:
                document['_id'] = str(document['_id'])
                theme = mongo.db.theme.find_one({"idtheme": document["idtheme"]},{"_id": False, "theme": True})
                auteur = mongo.db.auteur.find_one({"id_auteur": document["id_auteur"]}, {"_id": False})
                full_data = {**document, **theme, **auteur}
                response.append(full_data)
            return render_template("livre.html", response=response), 200
        except Exception as e:
             return jsonify({'ok': False, 'message': str(e)}), 500
