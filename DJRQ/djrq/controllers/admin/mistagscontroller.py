import djrq.middleware
import web
from djrq.model import *

class MistagsController(web.core.Controller):
    def __after__(self, *args, **kw):
        mistags = session.query(Mistags)
        for m in mistags:
            corrected = True
            if m.song.artist.fullname != m.artist:
                corrected = False
            if m.song.album.fullname != m.album:
                corrected = False
            if m.song.title != m.title:
                corrected = False
            if corrected:
                session.delete(m)
        return super(MistagsController, self).__after__(('djrq.templates.admin.mistags', 
                                                             dict(mistags=mistags)))

    def index(self, *args, **kw):
        pass

    def delete(self, *args, **kw):
        delmistag = session.query(Mistags).filter(Mistags.id==args[0]).one()
        session.delete(delmistag)
        pass
