from flask import jsonify, g
from app.models import User
from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth("Bearer")


@auth.verify_token
def verify_auth_token(token):
    g.user = User.decode_auth_token(token)
    if g.user is None:
        return False
    else:
        return True


@auth.error_handler
def invalid_token():
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': 'please send your authentication token'})
    response.status_code = 401
    return response
