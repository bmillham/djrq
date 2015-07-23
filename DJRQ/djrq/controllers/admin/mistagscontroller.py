import djrq.middleware
import web
from djrq.model import *
from ..basecontroller import BaseController

class MistagsController(BaseController):
    def __after__(self, rkw, *args, **kw):
        mistags = session.query(Mistags)
        for m in mistags:
            corrected = True
            if m.song is None: # Mistag was probably fixed, or the track was removed
                session.delete(m)
                continue
            if m.song.artist.fullname != m.artist:
                corrected = False
            if m.song.album.fullname != m.album:
                corrected = False
            if m.song.title != m.title:
                corrected = False
            if corrected:
                session.delete(m)
        return super(MistagsController, self).__after__(('djrq.templates.admin.mistags', 
                                                             dict(rkw, mistags=mistags)))

    def index(self, *args, **kw):
        return kw

    def delete(self, *args, **kw):
        delmistag = session.query(Mistags).filter(Mistags.id==args[0]).one()
        session.delete(delmistag)
        return kw
