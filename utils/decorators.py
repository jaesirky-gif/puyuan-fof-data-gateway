import functools

from flask import g, request
from bases.exceptions import LogicError, AuthError, AuthPermissionError


def login_required(func):
    @functools.wraps(func)
    def _func_wrapper(cls, *args, **kwargs):
        from apps.auth.authtoken import TokenAuthentication
        token = TokenAuthentication().authenticate(request)
        g.token = token

        return func(cls, *args, **kwargs)
    return _func_wrapper


def params_required(*params, **type_params):
    def dec(func):

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            for arg in params:
                if getattr(self.input, arg) is None:
                    raise LogicError('需要:%s 参数' % arg)
                if getattr(self.input, arg) == '':
                    raise LogicError('参数:%s 不能为空' % arg)
            for k, _type in type_params.items():
                if getattr(self.input, k) is None:
                    raise LogicError('需要:%s 参数' % k)
                if getattr(self.input, k) == '':
                    raise LogicError('参数:%s 不能为空' % k)
                if not isinstance(getattr(self.input, k), _type):
                    raise LogicError('参数 "%s" 类型应该是: %s' % (k, _type))

            return func(self, *args, **kwargs)
        return wrapper
    return dec
