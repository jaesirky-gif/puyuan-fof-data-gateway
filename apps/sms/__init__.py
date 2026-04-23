from flask import Blueprint
from flask_restful import Api
from .view import MobileSMSAPI, NavSMSAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/sms')
api = Api(blu)

api.add_resource(MobileSMSAPI, '/mobile_code')
api.add_resource(NavSMSAPI, '/nav')

