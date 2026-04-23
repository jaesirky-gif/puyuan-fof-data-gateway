from flask import Blueprint
from flask_restful import Api
from .view import FOFPublicInfoAPI, FOFPublicNavAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/fof')
api = Api(blu)

api.add_resource(FOFPublicInfoAPI, '/public/info/<string:fof_id>')
api.add_resource(FOFPublicNavAPI, '/public/nav/<string:fof_id>')

