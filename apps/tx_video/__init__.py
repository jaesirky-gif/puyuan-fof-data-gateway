from flask import Blueprint
from flask_restful import Api
from .view import UserSigAPI, ParseVideoUrlAPI,\
    StartMixVideoAPI, StopMixVideoAPI, SaveVideoCallBackAPI, CallMixVideoAPI

blu = Blueprint('{}_blu'.format(__name__), __name__, url_prefix='/api/v1/tx_video')
api = Api(blu)

api.add_resource(UserSigAPI, '/user_sig')
api.add_resource(ParseVideoUrlAPI, '/parse')
api.add_resource(CallMixVideoAPI, '/call')
api.add_resource(StartMixVideoAPI, '/start')
api.add_resource(StopMixVideoAPI, '/stop')
api.add_resource(SaveVideoCallBackAPI, '/save_video_cb')

