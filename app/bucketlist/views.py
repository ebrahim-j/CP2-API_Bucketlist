import json
from app.models import User, Bucketlist, Item
from app.bucketlist import bucketlist_blueprint
from flask import g, jsonify, request
from app import db



@bucketlist_blueprint.route('/api/bucketlists/', methods=['POST'])
def create_bucketlist():
    try:
        name = request.json.get("name")
    except KeyError:
        return jsonify({"error": "missing bucketlist name"}), 400

    if not name:
        return jsonify({"error": "bucketlist name cannot be empty"}), 400

    bucketlist = Bucketlist.query.filter_by(name=name).first()
    if bucketlist:
        return jsonify({"error": "bucketlist with a similar name exists"}), 400

    user_id = g.user.id
    bucketlist = Bucketlist(name=name, created_by=user_id)
    db.session.add(bucketlist)
    db.session.commit()
    return jsonify({"message": "created bucketlist '" + name + "'"}), 201

@bucketlist_blueprint.route('/api/bucketlists/', methods=['GET'])
def list_bucketlists():
    return "This"

@bucketlist_blueprint.route('/api/bucketlists/<int:bucketlist_id>/', methods=['GET'])
def get_bucketlist_by_id(bucketlist_id):
    return "This"

@bucketlist_blueprint.route('/api/bucketlists/<int:bucketlist_id>/', methods=['PUT'])
def update_bucketlist(bucketlist_id):
    return "This"

@bucketlist_blueprint.route('/api/bucketlists/<int:bucketlist_id>/items/', methods=['POST'])
def create_bucketlist_item(bucketlist_id):
    return "This"

@bucketlist_blueprint.route('/api/bucketlists/<int:bucketlist_id>/items/<int:item_id>/', methods=['PUT'])
def update_bucketlist_item(bucketlist_id, item_id):
    return "This"

@bucketlist_blueprint.route('/api/bucketlists/<int:bucketlist_id>/', methods=['DELETE'])
def delete_bucketlist(bucketlist_id):
    return "This"

@bucketlist_blueprint.route('/api/bucketlists/<int:bucketlist_id>/items/<int:item_id>/', methods=['DELETE'])
def delete_bucketlist_item(bucketlist_id, item_id):
    return "This"

# edge cases here