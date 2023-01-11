"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
# jackson_family.add_member({
#     "id": jackson_family._generateId(),
#     "first_name": "John",
#     "last_name": "Jackson",
#     "age": 33,
#     "lucky_numbers": [7, 13, 22]

# })

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }

    return jsonify(response_body), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_single_member(id):
    member = jackson_family.query.filter(jackson_family.id == member).first()
    if member is None:
        return jsonify({"member was not found"}), 404
    return jsonify(member,200)

@app.route('/members', methods=['POST'])
def add_member():
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    age = request.json.get("age")
    lucky_numbers = request.json.get("lucky_numbers")

    if not first_name:
        return jsonify({"you must add a first name"}), 400
    if not last_name:
        return jsonify({"you must add a last name"}), 400
    if not age:
        return jsonify({"you must add age"}), 400
    if not lucky_numbers:
        return jsonify({"you must add lucky_numbers"}), 400

    new_member = {
        "id": request.json.get("id") if request.json.get("id") is not None else jackson_family._generateId(),
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "lucky_numbers": lucky_numbers
    }
    response = jackson_family.add_member(new_member)
    return jsonify({"new member added": response})


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
