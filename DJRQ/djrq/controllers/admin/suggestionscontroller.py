import djrq.middleware
import web
from djrq.model import *

class SuggestionsController(web.core.Controller):
    def __after__(self, *args, **kw):
        suggestions = session.query(Suggestions)
        return super(SuggestionsController, self).__after__(('djrq.templates.admin.suggestions', 
                                                             dict(suggestions=suggestions)))

    def index(self, *args, **kw):
        pass

    def delete(self, *args, **kw):
        delsuggestion = session.query(Suggestions).filter(Suggestions.id==args[0]).one()
        session.delete(delsuggestion)
        pass
