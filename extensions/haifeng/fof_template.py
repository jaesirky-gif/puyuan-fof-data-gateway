
import requests

from flask import current_app

from bases.constants import HaiFengTemplateType
from bases.exceptions import LogicError
from bases.globals import db, settings
from models import FOFInfo

from .haifeng_token import HaiFengToken


class FOFTemplate:

    def __init__(self):
        self.host = settings['HAI_FENG']['host']

    def _parse_data(self, data):
        if data['success'] != 1:
            current_app.logger.error(f'[FOFTemplate] Failed! (data){data}')
            return
        return data['data']

    def request(self, endpoint, params=None):
        headers = HaiFengToken().get_headers()
        response = requests.post(self.host + endpoint, json=params, timeout=10, headers=headers)

        data = response.text
        current_app.logger.info(f'[FOFTemplate] (endpoint){endpoint} (data){data} (params){params}')
        return data, response.status_code
