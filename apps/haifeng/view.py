import datetime
import pandas as pd
import empyrical as ep
from flask import make_response, request

from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required, params_required
from extensions.haifeng.fof_template import FOFTemplate
from extensions.haifeng.haifeng_token import HaiFengToken


class HFTransAPI(ApiViewHandler):

    @params_required(*['endpoint'])
    @login_required
    def post(self):
        data, status_code = FOFTemplate().request(
            self.input.endpoint,
            request.json.get('params'),
        )
        res = make_response(data, status_code)
        res.headers["Content-type"] = "application/json"
        return res


class HaiFengTokenAPI(ApiViewHandler):

    @login_required
    def get(self):
        return HaiFengToken().get_token()


class HaiFengHeadersAPI(ApiViewHandler):

    @login_required
    def get(self):
        return HaiFengToken().get_headers()

