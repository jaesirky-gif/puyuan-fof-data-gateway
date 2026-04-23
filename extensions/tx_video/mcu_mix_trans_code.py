import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.trtc.v20190722 import trtc_client, models
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


class MCUMixTransCode:

    def __init__(self, app_id, sec_id, sec_key):
        self.app_id = int(app_id)
        cred = credential.Credential(sec_id, sec_key)

        http_profile = HttpProfile()
        http_profile.endpoint = "trtc.tencentcloudapi.com"

        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile
        self.client = trtc_client.TrtcClient(cred, "ap-beijing", client_profile)

    def start_mix(self, room_id, stream_id, investor_id, adviser_id):
        try:
            req = models.StartMCUMixTranscodeByStrRoomIdRequest()
            params = {
                'SdkAppId': self.app_id,
                'StrRoomId': str(room_id),
                'OutputParams': {
                    'StreamId': stream_id,
                    'RecordId': stream_id + '_file',
                },
                'LayoutParams': {
                    'Template': 3,
                    'MainVideoUserId': investor_id,
                    'MainVideoStreamType': 0,
                    'SmallVideoLayoutParams': {
                        'UserId': str(adviser_id),
                        'StreamType': 0,
                        'ImageWidth': 90,
                        'ImageHeight': 180,
                        'LocationX': 283,
                        'LocationY': 630,
                    },
                },
                'EncodeParams': {
                    'AudioSampleRate': 48000,
                    'AudioBitrate': 64,
                    'AudioChannels': 2,
                    'VideoWidth': 375,
                    'VideoHeight': 812,
                    'VideoBitrate': 1560,
                    'VideoFramerate': 15,
                    'VideoGop': 2,
                }
            }
            req.from_json_string(json.dumps(params))

            resp = self.client.StartMCUMixTranscodeByStrRoomId(req)
            print(resp.to_json_string())
            return True
        except TencentCloudSDKException as err:
            print(err)
            return False

    def stop_mix(self, room_id):
        try:
            req = models.StopMCUMixTranscodeByStrRoomIdRequest()
            params = {
                'SdkAppId': self.app_id,
                'StrRoomId': str(room_id),
            }
            req.from_json_string(json.dumps(params))

            resp = self.client.StopMCUMixTranscodeByStrRoomId(req)
            print(resp.to_json_string())
            return True
        except TencentCloudSDKException as err:
            print(err)
            return False

