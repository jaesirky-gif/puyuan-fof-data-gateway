from flask import current_app, request, g

from bases.viewhandler import ApiViewHandler
from bases.globals import settings, db
from bases.exceptions import VerifyError
from utils.decorators import login_required, params_required
from models import VideoRoom
from extensions.tx_video.tls_sig_api_v2 import TLSSigAPIv2
from extensions.tx_video.mcu_mix_trans_code import MCUMixTransCode
from extensions.tx_video.video_key import VideoKey


class SaveVideoCallBackAPI(ApiViewHandler):

    def deal_main(self, obj, user_id):
        if str(obj.adviser_id) == str(user_id):
            obj.adviser_url = self.input.video_url
            obj.save()
        elif obj.investor_id == user_id:
            obj.investor_url = self.input.video_url
            obj.save()

    @params_required(*['stream_id', 'video_url'])
    def post(self):
        current_app.logger.info(request.json)
        app_id, room_id, user_id, way = self.input.stream_id.split('_')

        obj = VideoRoom.get_by_id(room_id)

        if way == 'main':
            self.deal_main(obj, user_id)
        elif way == 'mix':
            obj.video_url = self.input.video_url
            obj.save()


class CallMixVideoAPI(ApiViewHandler):

    @params_required(*['room_id'])
    @login_required
    def post(self):
        obj = VideoRoom.filter_by_query(
            id=self.input.room_id,
        ).first()
        if not obj:
            return {
                'status': VideoRoom.VideoStatus.NOTHING,
            }
        return obj.to_dict()


class StopMixVideoAPI(ApiViewHandler):

    @params_required(*['room_id', 'manager_id', 'adviser_id', 'investor_id'])
    @login_required
    def post(self):
        obj = VideoRoom.filter_by_query(
            id=self.input.room_id,
            manager_id=self.input.manager_id,
            adviser_id=self.input.adviser_id,
            investor_id=self.input.investor_id,
        ).first()
        if not obj:
            raise VerifyError('混流未开始！')

        m = MCUMixTransCode(
            settings['TX_VIDEO']['app_id'],
            settings['TX_VIDEO']['sec_id'],
            settings['TX_VIDEO']['sec_key'],
        )
        status = m.stop_mix(self.input.room_id)
        if not status:
            raise VerifyError('混流结束失败！')


class StartMixVideoAPI(ApiViewHandler):

    @params_required(*['room_id', 'manager_id', 'adviser_id', 'investor_id'])
    @login_required
    def post(self):
        obj = VideoRoom.filter_by_query(
            id=self.input.room_id,
            manager_id=self.input.manager_id,
            adviser_id=self.input.adviser_id,
            investor_id=self.input.investor_id,
        ).first()
        if not obj:
            obj = VideoRoom.create(
                id=self.input.room_id,
                manager_id=self.input.manager_id,
                adviser_id=self.input.adviser_id,
                investor_id=self.input.investor_id,
            )

        m = MCUMixTransCode(
            settings['TX_VIDEO']['app_id'],
            settings['TX_VIDEO']['sec_id'],
            settings['TX_VIDEO']['sec_key'],
        )
        status = m.start_mix(
            self.input.room_id,
            stream_id='{}_{}_{}_mix'.format(settings['TX_VIDEO']['app_id'], self.input.room_id, obj.investor_id),
            investor_id=obj.investor_id,
            adviser_id=obj.adviser_id,
        )
        if not status:
            raise VerifyError('混流开始失败！')


class ParseVideoUrlAPI(ApiViewHandler):

    @params_required(*['room_id'])
    @login_required
    def post(self):
        obj = VideoRoom.filter_by_query(
            id=self.input.room_id,
        ).first()
        if not obj:
            raise VerifyError('视频号错误')

        if not obj.video_url:
            raise VerifyError('视频未录制')

        url = VideoKey(settings['TX_VIDEO']['view_key']).create(obj.video_url)
        return {
            'url': url
        }


class UserSigAPI(ApiViewHandler):

    @params_required(*['user_id'])
    @login_required
    def post(self):
        t = TLSSigAPIv2(
            sdkappid=settings['TX_VIDEO']['app_id'],
            key=settings['TX_VIDEO']['app_sec'],
        )
        sig = t.genUserSig(self.input.user_id)
        return {
            'app_id': settings['TX_VIDEO']['app_id'],
            'sig': sig,
        }

