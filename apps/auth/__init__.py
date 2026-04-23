from flask import Blueprint
from flask_restful import Api
from .view import TokenAPI, TokenCheckAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/token')
api = Api(blu)

api.add_resource(TokenAPI, '/gen')
api.add_resource(TokenCheckAPI, '/check')

