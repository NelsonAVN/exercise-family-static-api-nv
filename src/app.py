"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):

    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(member_id)
    
    if not member:
        return jsonify({"Error" : "the member doesn't exist"}), 404 
    return jsonify(member), 200

@app.route('/member', methods=['POST'])
def add_member():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    request_data = request.get_json()
    
    if 'first_name' not in request_data or 'age' not in request_data or 'lucky_numbers' not in request_data:
        return jsonify({"error": "Missing data"}), 400

    try:
        new_member = {
            "first_name": request_data['first_name'],
            "age": request_data['age'],
            "lucky_numbers": request_data['lucky_numbers']
        }
    except KeyError as e:
        return jsonify({"error": f"Missing {e.args[0]}"}), 400

    jackson_family.add_member(new_member)
    return jsonify(new_member), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
        member = jackson_family.get_member(member_id)
        if not member: 
            return jsonify({"error": "Member not found"}), 404
        jackson_family.delete_member(member_id)
        return jsonify({"message": "Member deleted successfully"}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
