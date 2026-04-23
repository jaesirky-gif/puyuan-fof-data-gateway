import datetime
import pandas as pd
import empyrical as ep
from flask import request

from bases.constants import SMS
from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required, params_required
from bases.exceptions import VerifyError
from extensions.mengwang.sms import MWMassage
from .libs import send_sms


class MobileSMSAPI(ApiViewHandler):

    @params_required(*['mobile', 'mobile_code'])
    @login_required
    def post(self):
        sms_template = SMS.LOGIN if not request.json.get('sms_template') else request.json.get('sms_template')
        status, msg = send_sms(
            mobile=self.input.mobile,
            mobile_code=self.input.mobile_code,
            sms_template=sms_template,
        )
        if not status:
            raise VerifyError(msg)


class NavSMSAPI(ApiViewHandler):

    @params_required(*['send_to', 'data'])
    @login_required
    def post(self):
        try:
            cli = MWMassage()
            cli.single_send(
                self.input.send_to,
                self.input.data,
            )
        except Exception as e:
            raise VerifyError('发送短信失败')

