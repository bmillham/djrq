import djrq.middleware
import web
from djrq.model import *
from basecontroller import BaseController

class AlbumController(BaseController):
    def id(self, *args, **kwargs):
        a = session.query(Album).filter(Album.id == args[0]).one()
        return "djrq.templates.album", dict(album=a,
                                            listeners=kwargs['listeners'],
                                                   current_page="album",
                                                   limit_requests=kwargs['limit_requests'],
                                                   show_title=kwargs['show_title'],
                                                   start_time=kwargs['start_time'],
                                                   requests_count=get_new_pending_requests_info()[0])
