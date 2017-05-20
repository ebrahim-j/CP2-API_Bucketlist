from flask import Blueprint, g
from ..authentication import auth


bucketlist_blueprint = Blueprint('bucketlist_blueprint', __name__)


@bucketlist_blueprint.before_request
@auth.login_required
def before_request():
    """ Add authentication to all endpoints accessed using this blueprint """
    pass

from . import views
