from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    from app.models import Bucketlist, User, Item
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    @app.route('/bucketlists/', methods=['POST', 'GET'])
    def bucketlists():
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        

        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            # print (user_id)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authenticated

                if request.method == "POST":
                    name = str(request.data.get('name', ''))
                    if name:
                        bucketlist = Bucketlist(name=name, created_by=user_id)
                        bucketlist.save()
                        response = jsonify({
                            'id': bucketlist.id,
                            'name': bucketlist.name,
                            'date_created': bucketlist.date_created,
                            'date_modified': bucketlist.date_modified,
                            'created_by': user_id
                        })

                        return make_response(response), 201
                    else:
                        response = jsonify({
                            "message": "Humans baffle me... Kweni you want to do nothing?"
                        })
                        return make_response(response), 400

                else:
                    # GET all the bucketlists created by this user
                    bucketlists = Bucketlist.query.filter_by(created_by=user_id)
                    if bucketlists:
                        results = []

                        for bucketlist in bucketlists:
                            items = Item.query.filter_by(bucketlist_id=bucketlist.id)
                            results_items = []
                            for item in items:
                                obj = {
                                    'id': item.item_id,
                                    'name': item.name,
                                    'date_created': item.date_created,
                                    'date_modified': item.date_modified
                                }
                                results_items.append(obj)
                            obj = {
                                'id': bucketlist.id,
                                'name': bucketlist.name,
                                'date_created': bucketlist.date_created,
                                'date_modified': bucketlist.date_modified,
                                'items': results_items,
                                'created_by': bucketlist.created_by
                            }
                            results.append(obj)

                        return make_response(jsonify(results)), 200
                    else:
                        response = jsonify({
                            "message": "No bucketlist yet"
                        })
                        return make_response(response), 400
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(id, **kwargs):
     # retrieve a buckelist using it's ID
        # get the access token from the authorization header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            # Get the user id related to this access token
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                # If the id is not a string(error), we have a user id
                # Get the bucketlist with the id specified from the URL (<int:id>)
                bucketlist = Bucketlist.query.filter_by(created_by=user_id).first()
                if not bucketlist:
                    # There is no bucketlist with this ID for this User, so
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)

                if request.method == "DELETE":
                    # delete the bucketlist using our delete method
                    bucketlist.delete()
                    return {
                        "message": "bucketlist {} deleted".format(bucketlist.id)
                    }, 200

                elif request.method == 'PUT':
                    # Obtain the new name of the bucketlist from the request data
                    name = str(request.data.get('name', ''))

                    bucketlist.name = name
                    bucketlist.save()

                    response = {
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'created_by': bucketlist.created_by
                    }
                    return make_response(jsonify(response)), 200
                else:
                    # Handle GET request, sending back the bucketlist to the user
                    items = Item.query.filter_by(bucketlist_id=id)
                    results_items = []
                    
                    for item in items:
                        obj = {
                            'id': item.item_id,
                            'name': item.name,
                            'date_created': item.date_created,
                            'date_modified': item.date_modified
                        }
                        results_items.append(obj)
                    obj = {
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'items': results_items,
                        'created_by': bucketlist.created_by
                    }

                    return make_response(jsonify(obj)), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                # return an error response, telling the user he is Unauthorized
                return make_response(jsonify(response)), 401
    
    @app.route('/bucketlists/<int:id>/items/', methods=['POST'])
    def items(id, **kwargs):
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        

        if access_token:
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                # If the id is not a string(error), we have a user id
                # Get the bucketlist with the id specified from the URL (<int:id>)
                bucketlist = Bucketlist.query.filter_by(id=id).first()
                if not bucketlist:
                    # There is no bucketlist with this ID for this User, so
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)
                name = str(request.data.get('name', ''))
                if name:
                    item = Item(name=name, bucketlist_id=id)
                    item.save()
                    response = jsonify({
                        'id': item.item_id,
                        'name': item.name,
                        'date_created': item.date_created,
                        'date_modified': item.date_modified
                    })

                    return make_response(response), 201
                else:
                    response = jsonify({
                        "message": "Item must have name"
                    })
                    return make_response(response), 400

            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                # return an error response, telling the user he is Unauthorized
                return make_response(jsonify(response)), 401


    @app.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT', 'DELETE'])
    def items_manipulation(id, item_id, **kwargs):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        

        if access_token:
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                bucketlist = Bucketlist.query.filter_by(id=id).first()
                if not bucketlist:
                    # There is no bucketlist with this ID for this User, so
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)


                item = Item.query.filter_by(item_id=item_id).first()
                if not item:
                    # There is no bucketlist with this ID for this User, so
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)

                if request.method == "DELETE":
                    # delete the bucketlist using our delete method
                    item.delete()
                    return {
                        "message": "Item deleted successfully"
                    }, 200
                
                elif request.method == 'PUT':
                    # Obtain the new name of the bucketlist from the request data
                    name = str(request.data.get('name', ''))

                    if name:
                        item.name = name
                        item.save()

                        response = {
                            'id': item.item_id,
                            'name': item.name,
                            'date_created': item.date_created,
                            'date_modified': item.date_modified
                        }
                        return make_response(jsonify(response)), 200
                    else:
                        response = jsonify({
                            "message": "Item name not valid"
                        })
                        return make_response(response), 400

                
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                # return an error response, telling the user he is Unauthorized
                return make_response(jsonify(response)), 401




    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app
