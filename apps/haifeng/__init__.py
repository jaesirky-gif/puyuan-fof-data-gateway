from flask import Blueprint
from flask_restful import Api
from .view import HFTransAPI, HaiFengTokenAPI, HaiFengHeadersAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/hf')
api = Api(blu)

api.add_resource(HFTransAPI, '/trans')
api.add_resource(HaiFengTokenAPI, '/token')
api.add_resource(HaiFengHeadersAPI, '/headers')

