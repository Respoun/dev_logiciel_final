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

    # if request.method == 'POST':
    #     data = request.get_json(force=True)
    #     if data.get('id', None) is not None and data.get('client_id', None) is not None and data.get('sum', None) is not None:
    #         mongo.db.Test.insert_one(data)
    #         return jsonify({'ok': True, 'message': 'Bills created successfully!'}), 200
    #     else:
    #         return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
    #
    # if request.method == 'DELETE':
    #     if data.get('id', None) is not None:
    #         db_response = mongo.db.Test.delete_one({'id': data['id']})
    #         if db_response.deleted_count == 1:
    #             response = {'ok': True, 'message': 'record deleted'}
    #         else:
    #             response = {'ok': True, 'message': 'no record found'}
    #         return jsonify(response), 200
    #     else:
    #         return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
    #
    # if request.method == 'PATCH':
    #     data = request.get_json(force=True)
    #     if data.get('query', {}) != {}:
    #         mongo.db.Test.update_one(
    #             data['query'], {'$set': data.get('payload', {})})
    #         return jsonify({'ok': True, 'message': 'record updated'}), 200
    #     else:
    #         return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
