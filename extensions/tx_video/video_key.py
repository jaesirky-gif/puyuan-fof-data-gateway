import hashlib
import random
import string
import time


class VideoKey:

    def __init__(self, key):
        self.key = key

    def create(self, url):
        file_keys = url.split('/')
        file_key = '/{}/{}/'.format(file_keys[3], file_keys[4])
        t = str(hex(int(time.time()) + 60 * 60 * 2))[2:]
        nonce = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
        r_limit = 3
        sign_string = '{}{}{}{}{}'.format(
            self.key,
            file_key,
            t,
            r_limit,
            nonce,
        )
        sign = hashlib.md5(sign_string.encode()).hexdigest()
        ret_url = url + '?t={}&rlimit={}&us={}&sign={}'.format(t, r_limit, nonce, sign)

        return ret_url



if __name__ == '__main__':
    VideoKey('1').create('http://1306034002.vod2.myqcloud.com/51b47655vodcq1306034002/d96232585285890818930958722/0axUTTF8hkMA.mp4')