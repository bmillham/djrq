import djrq.middleware
import web
from djrq.model import *

class MistagsController(web.core.Controller):
    def __after__(self, *args, **kw):
        mistags = session.query(Mistags)
        return super(MistagsController, self).__after__(('djrq.templates.admin.mistags', 
                                                             dict(mistags=mistags)))

    def index(self, *args, **kw):
        pass

    def delete(self, *args, **kw):
        delmistag = session.query(Mistags).filter(Mistags.id==args[0]).one()
        session.delete(delmistag)
        pass
