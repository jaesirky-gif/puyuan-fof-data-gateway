import jwt
import datetime
import time


class JWTToken:

    @staticmethod
    def encode(payload: dict, secret_key: str, expires=None):
        """
        生成认证Token
        :param payload: dict
        :param secret_key:
        :param expires
        :return: string
        """
        if expires:
            payload['exp'] = expires

        return jwt.encode(
            payload,
            secret_key,
        )

    @staticmethod
    def decode(token, secret_key):
        """
        验证Token
        :param token:
        :param secret_key
        :return: True|False, integer|string
        """
        try:
            # payload = jwt.decode(token, secret_key, leeway=datetime.timedelta(seconds=1), algorithms=["HS256"])
            payload = jwt.decode(token, secret_key, options={'verify_exp': False}, algorithms=["HS256"])

            # 过期验证
            if payload['exp'] < int(str(time.time())[:10]):
                raise jwt.ExpiredSignatureError
            # 参数对验证
            if 'data' in payload:
                return True, payload
            raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return False, 'Token过期'
        except jwt.InvalidTokenError:
            return False, '无效Token'


if __name__ == '__main__':
    # print(datetime.datetime.utcnow())
    # print(datetime.datetime.now())
    #
    #
    s = JWTToken.encode({
        'data': {'hhh': 3},
        # 'iat': datetime.datetime.utcnow(),
        # 'exp': datetime.datetime.now() + datetime.timedelta(seconds=5),
    }, '6u9HzUJIhOG6jmNFytNlbr2angjiooajgoajgu', datetime.datetime.utcnow() + datetime.timedelta(seconds=5))
    print(s)
    time.sleep(3)
    # s = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoX2lkIjoxLCJhdXRoX2lwIjoiMC4wLjAuMCIsImV4cCI6MTYyNDAyNTQ3Mn0.GC6gqVjDbj31fEj9bv3KdHzCcIBajqgXfeuheXTNIMs'
    print(JWTToken.decode(s, '6u9HzUJIhOG6jmNFytNlbr2angjiooajgoajgu'))
    time.sleep(3)
    print(JWTToken.decode(s, '6u9HzUJIhOG6jmNFytNlbr2angjiooajgoajgu'))


