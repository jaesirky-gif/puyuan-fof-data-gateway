from flask import Blueprint
from flask_restful import Api
from .view import FundListAPI, FundPointQueryAPI, FundSearcherAPI, FOFPriFundSearcherAPI, FundScreenAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/')
api = Api(blu)

api.add_resource(FOFPriFundSearcherAPI, '/management_search/<string:key_word>')
api.add_resource(FundSearcherAPI, 'funds/searcher/<string:key_word>')
api.add_resource(FundListAPI, 'fund/list')
api.add_resource(FundPointQueryAPI, 'fund/point_query')
api.add_resource(FundScreenAPI, 'fund/screen')
