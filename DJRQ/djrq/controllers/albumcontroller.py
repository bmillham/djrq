import djrq.middleware
import web
from ..model import session
from ..model.helpers import get_artist_letters_counts, get_new_pending_requests_info
from ..model.song import Song
from basecontroller import BaseController

class AlbumController(BaseController):
    def id(self, *args, **kwargs):
        from ..model.album import Album

        a = session.query(Album).filter(Album.id == args[0]).one()
        return "djrq.templates.album", dict(album=a,
                                            songs=a.songs,
                                            listeners=kwargs['listeners'],
                                                   current_page="album",
                                                   limit_requests=kwargs['limit_requests'],
                                                   show_title=kwargs['show_title'],
                                                   start_time=kwargs['start_time'],
                                                   requests_count=get_new_pending_requests_info()[0])

    def name(self, *args, **kwargs):
        s = session.query(Song).filter(Song.album_fullname==args[0]).order_by(Song.track)
        return "djrq.templates.album", dict(album=s[0].album,
                                            listeners=kwargs['listeners'],
                                                   current_page="album",
                                                   limit_requests=kwargs['limit_requests'],
                                                   show_title=kwargs['show_title'],
                                                   start_time=kwargs['start_time'],
                                                   songs=s,
                                                   requests_count=get_new_pending_requests_info()[0])