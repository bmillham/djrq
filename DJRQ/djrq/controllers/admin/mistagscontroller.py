import djrq.middleware
import web
from ...model import session
from ...model.mistags import Mistags
from ..basecontroller import BaseController
from web.auth import authorize
from account import AccountMixIn

class MistagsController(BaseController, AccountMixIn):
    def __after__(self, *args, **kw):
         # if args[0] is a tuple, then this was a redirect, otherwise it was a normal request
        try:
            temp, k = args[0]
        except:
            k = args[0]
            temp = 'djrq.templates.admin.mistags'
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
        return super(MistagsController, self).__after__((temp,
                                                             dict(k, mistags=mistags)))

    @authorize(web.auth.authenticated)
    def index(self, *args, **kw):
        return kw

    @authorize(web.auth.authenticated)
    def delete(self, *args, **kw):
        delmistag = session.query(Mistags).filter(Mistags.id==args[0]).one()
        session.delete(delmistag)
        return kw
