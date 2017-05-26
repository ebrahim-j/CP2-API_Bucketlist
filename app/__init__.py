from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

from instance.config import app_config
db = SQLAlchemy()


def create_app(config_name):
    """ Creates the app based on the configurations"""
    from app.models import Bucketlist, User, Item
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/api/v1/bucketlists/', methods=['POST', 'GET'])
    def bucketlists():
        """ Creates a bucketlis(POST) or
         lists all bucketlists(GET) for a user"""
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            response = jsonify({
                "message": "You do not have access to this resource"
            })
            return make_response(response), 401
        access_token = auth_header.split(" ")[1]
        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            # print (user_id)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authenticated
                if request.method == "POST":
                    all_buckets = Bucketlist.query.filter_by(created_by=user_id)
                    named_buckets = [bucket.name.upper()
                                     for bucket in all_buckets]
                    name = str(request.data.get('name', ''))
                    if name:
                        # check if name already exists
                        if name.upper() in named_buckets:
                            response = jsonify({
                                "message": "Bucketlist with that name exists"
                            })
                            return make_response(response), 400

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
                            "message": "Bucketlist must have name"
                        })
                        return make_response(response), 400

                else:
                    # GET bucketlist by name
                    search = str(request.args.get('q', ''))
                    if search:
                        bucketlist = Bucketlist.query.filter_by(
                            name=search).filter_by(created_by=user_id).first()

                        if not bucketlist:
                            # There is no bucketlist with this ID for this User, so
                            # Raise an HTTPException with a 404 not found
                            # status code
                            obj = {
                                "message": "No bucketlist found with that name. Remember: Names are spelling+case sensitive"
                            }
                            return make_response(jsonify(obj)), 400
                        else:
                            items = Item.query.filter_by(
                                bucketlist_id=bucketlist.id)
                            results_items = []
                            if items:

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
                        # GET all the bucketlists created by this user
                        if request.args.get("page"):
                            page = int(request.args.get("page"))
                        else:
                            page = 1
                        if request.args.get("limit") and int(request.args.get("limit")) < 100:
                            limit = int(request.args.get("limit"))
                        else:
                            limit = 3
                        bucketlists = Bucketlist.query.filter_by(
                            created_by=user_id).paginate(page, limit, False)
                        listed_bucketlists = bucketlists.items
                        if bucketlists.has_next:
                            nextpage = "/api/v1/bucketlists/?page=" + \
                                str(page + 1) + "&limit=" + str(limit)
                        else:
                            nextpage = None
                        if bucketlists.has_prev:
                            previouspage = "/api/v1/bucketlists/?page=" + \
                                str(page - 1) + "&limit=" + str(limit)
                        else:
                            previouspage = None

                        if bucketlists:
                            temp_list = []
                            for bucketlist in listed_bucketlists:
                                items = Item.query.filter_by(
                                    bucketlist_id=bucketlist.id)
                                results_items = []
                                for item in items:
                                    obj = {
                                        'id': item.item_id,
                                        'name': item.name,
                                        'date_created': item.date_created,
                                        'date_modified': item.date_modified
                                    }
                                    results_items.append(obj)
                                data = {
                                    'id': bucketlist.id,
                                    'name': bucketlist.name,
                                    'date_created': bucketlist.date_created,
                                    'date_modified': bucketlist.date_modified,
                                    'items': results_items,
                                    'created_by': bucketlist.created_by
                                }
                                temp_list.append(data)
                            response = {
                                "next": nextpage,
                                "prev": previouspage,
                                "Buckets": temp_list
                            }
                            return make_response(jsonify(response)), 200

                        else:
                            response = jsonify({
                                "message": "No bucketlist yet"
                            })
                            return make_response(response), 404
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/api/v1/bucketlists/<int:b_id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(b_id, **kwargs):
        """ GETS a bucketlist's info, changes it or deletes it by ID"""

        # get the access token from the authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            response = jsonify({
                "message": "You do not have access to this resource"
            })
            return make_response(response), 401
        access_token = auth_header.split(" ")[1]

        if access_token:
            # Get the user id related to this access token
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                # If the id is not a string(error), we have a user id
                # Get the bucketlist with the id specified from the URL
                # (<int:b_id>)
                bucketlist = Bucketlist.query.filter_by(
                    created_by=user_id).filter_by(id=int(b_id)).first()
                if not bucketlist:
                    # There is no bucketlist with this ID for this User, so
                    # Raise an HTTPException with a 404 not found status code
                    response = jsonify({
                        "message": "This bucketlist is not there"
                    })
                    return make_response(response), 404

                if request.method == "DELETE":
                    # delete the bucketlist using our delete method
                    bucketlist.delete()
                    return {
                        "message": "bucketlist {} deleted".format(
                            bucketlist.id)
                    }, 200

                elif request.method == 'PUT':
                    # Obtain the new name of the bucketlist from the request
                    # data
                    name = str(request.data.get('name'))

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
                    # Handle GET request, sending back the bucketlist to the
                    # user
                    items = Item.query.filter_by(bucketlist_id=b_id)
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

    @app.route('/api/v1/bucketlists/<int:b_id>/items/', methods=['POST'])
    def items(b_id, **kwargs):
        """ Creates an item in a bucketlist """
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            response = jsonify({
                "message": "You do not have access to this resource"
            })
            return make_response(response), 401
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                # If the id is not a string(error), we have a user id
                # Get the bucketlist with the id specified from the URL
                # (<int:b_id>)
                bucketlist = Bucketlist.query.filter_by(id=b_id).first()
                if not bucketlist:
                    # There is no bucketlist with this ID for this User, so
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)
                name = str(request.data.get('name'))
                all_items = Item.query.filter_by(bucketlist_id=b_id)
                name_items = [item.name.upper() for item in all_items]
                if name:
                    if name.upper() in name_items:
                        response = jsonify({
                            "message": "Item with that name already exists"
                        })
                        return make_response(response), 400

                    item = Item(name=name, bucketlist_id=b_id)
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

    @app.route('/api/v1/bucketlists/<int:b_id>/items/<int:item_id>', methods=['PUT', 'DELETE'])
    def items_manipulation(b_id, item_id, **kwargs):
        """ Changes info for an item or deltes it by ID"""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            response = jsonify({
                "message": "You do not have access to this resource"
            })
            return make_response(response), 401
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                bucketlist = Bucketlist.query.filter_by(id=b_id).first()
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
                    # Obtain the new name of the bucketlist from the request
                    # data
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
