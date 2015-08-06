# encoding: utf-8

import web
from web.auth import authenticate, deauthenticate
from marrow.util.bunch import Bunch


from djrq import model as db


__all__ = ['join', 'recover', 'login', 'logout', 'AccountMixIn']
log = __import__('logging').getLogger(__name__)



class JoinMethod(web.core.HTTPMethod):
    def get(self):
        return "djrq.templates.admin.join", dict()

    def post(self, **kw):
        pass

join = JoinMethod()


class RecoverMethod(web.core.HTTPMethod):
    def get(self):
        return "djrq.templates.admin.recover", dict()

    def post(self, **kw):
        pass

recover = RecoverMethod()

class LoginMethod(web.core.HTTPMethod):
    def get(self, redirect=None, **kwargs):
        if redirect is None:
            referrer = web.core.request.referrer
            redirect = '/' if referrer.endswith(web.core.request.script_name) else referrer
        return "djrq.templates.admin.login", dict(kwargs, redirect=redirect)

    def post(self, **kw):
        data = Bunch(kw)
        if not web.auth.authenticate(data.username, data.password):
            return "djrq.templates.admin.login", dict(redirect=kw['redirect'])
        if data.redirect:
            raise web.core.http.HTTPFound(location=data.redirect)
        raise web.core.http.HTTPFound(location='/')

login = LoginMethod()


def logout(self, *args, **kwargs):
    web.auth.deauthenticate()
    raise web.core.http.HTTPSeeOther(location=web.core.request.referrer)


class AccountMixIn(object):
    join = join
    recover = recover
    login = login
    logout = logout
