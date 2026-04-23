import datetime
import time
from flask import g, request, current_app
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from bases.globals import settings
from models import AuthSecret
from utils.jwt_token import JWTToken
from utils.decorators import params_required, login_required


class TokenAPI(ApiViewHandler):

    @params_required(*['app_id', 'app_secret', 'manager_id'])
    def post(self):
        u = AuthSecret.filter_by_query(
            app_id=self.input.app_id,
        ).first()
        if not u:
            raise VerifyError('用户名或密码错误')

        u.last_auth_time = datetime.datetime.now()
        u.save()

        if not u.check_app_hash(self.input.app_secret):
            time.sleep(2)
            raise VerifyError('用户名或密码错误')

        data = {
            'data': {
                'manager_id': self.input.manager_id,
                'auth_id': u.id,
                'auth_ip': request.headers.get('X-Real-Ip') if request.headers.get('X-Real-Ip') else '0.0.0.0'
            }
        }
        token = JWTToken.encode(
            payload=data,
            secret_key=settings['AUTH_SECRET_KEY'],
            expires=datetime.datetime.now() + datetime.timedelta(seconds=settings['AUTH_TOKEN_EXPIRES'])
        )

        return {
            'token': token
        }


class TokenCheckAPI(ApiViewHandler):

    @login_required
    def get(self):
        print(g.token)
        return
