import djrq.middleware
import web
from web.auth import authorize
from djrq.model import *
from ..basecontroller import BaseController
from account import AccountMixIn


class SuggestionsController(BaseController, AccountMixIn):
    
    def __after__(self, *args, **kw):
        # if args[0] is a tuple, then this was a redirect, otherwise it was a normal request
        try:
            temp, k = args[0]
        except:
            k = args[0]
            temp = 'djrq.templates.admin.suggestions'
        k['suggestions'] = session.query(Suggestions)
        return super(SuggestionsController, self).__after__((temp, k))

    @authorize(web.auth.authenticated)
    def index(self, *args, **kw):
        return kw

    @authorize(web.auth.authenticated)
    def delete(self, *args, **kw):
        delsuggestion = session.query(Suggestions).filter(Suggestions.id==args[0]).one()
        session.delete(delsuggestion)
        return kw
