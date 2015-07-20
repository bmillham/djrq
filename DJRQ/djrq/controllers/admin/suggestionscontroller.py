import djrq.middleware
import web
from djrq.model import *
from ..basecontroller import BaseController

class SuggestionsController(BaseController):
    def __after__(self, rkw, *args, **kw):
        suggestions = session.query(Suggestions)
        return super(SuggestionsController, self).__after__(('djrq.templates.admin.suggestions', 
                                                             dict(rkw, suggestions=suggestions)))

    def index(self, *args, **kw):
        return kw

    def delete(self, *args, **kw):
        delsuggestion = session.query(Suggestions).filter(Suggestions.id==args[0]).one()
        session.delete(delsuggestion)
        return kw
