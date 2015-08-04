import djrq.middleware
import web
from web.auth import authorize
from djrq.model import *
from ..basecontroller import BaseController
from account import AccountMixIn


class SuggestionsController(BaseController, AccountMixIn):
    
    def __after__(self, *args, **kw):
        print args, kw
        #kw.update(rkw)
        kw['suggestions'] = session.query(Suggestions)
        return super(SuggestionsController, self).__after__(('djrq.templates.admin.suggestions', 
                                                             kw))
    @authorize(web.auth.authenticated)
    def index(self, *args, **kw):
        kw=kw
        print "index kw"
        #return kw
        pass

    @authorize(web.auth.authenticated)
    def delete(self, *args, **kw):
        delsuggestion = session.query(Suggestions).filter(Suggestions.id==args[0]).one()
        session.delete(delsuggestion)
        #return kw
