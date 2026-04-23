from flask import Blueprint
from flask_restful import Api
from .view import TradeDatesAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/basic')
api = Api(blu)

api.add_resource(TradeDatesAPI, '/trade_dates')

