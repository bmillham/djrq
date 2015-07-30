import djrq.middleware
import web
from djrq.model import *
from time import time
from basecontroller import BaseController

class ArtistController(BaseController):
    def __after__(self, result, *args, **kw):
        print "Browse after:", args, kw, result
        if result is None:
            result = ('djrq.templates.letters', dict(current_page='/browse/artist',
                                                     letter=None,
                                                     letters=get_artist_letters_counts(),
                                                     browse_by='artist',
                                                     a_list=None,
                                                     limit_requests=result['limit_requests'],
                                                     show_title=result['show_title'],
                                                     start_time=result['start_time'],
                                                     #listeners=kw['listeners'],
                                                     requests_count = get_new_pending_requests_info()[0]))
        else:
            result = ('djrq.templates.artist', dict(result,  # Extend what the individual controller returns.
                                                    #listeners=kw['listeners'],
                                                limit_requests=result['limit_requests'],
                                                   show_title=result['show_title'],
                                                   start_time=result['start_time'],
                                                requests_count = get_new_pending_requests_info()[0]))
        return super(ArtistController, self).__after__(result, *args, **kw)

    def index(self, *args, **kwargs):
         return None

    def id(self, *args, **kw):
        a = session.query(Artist).filter(Artist.id == args[0]).one()
        return dict(artist=a,
                    limit_requests=kw['limit_requests'],
                    show_title=kw['show_title'],
                    start_time=kw['start_time'],
                    songs=a.songs, current_page="artist", listeners=kw['listeners'],)

    def new(self, *args, **kw):
        id = int(args[0])
        try:
            days = int(args[1])
        except:
            days = 30
        start = int(time()) - (60 * 60 * 24 * days)
        a = session.query(Artist).filter(Artist.id == id, Song.addition_time >= start).first()
        new_songs = session.query(Song).filter(Song.artist_id == id, Song.addition_time >= start).order_by(Song.track)
        return dict(artist=a,
                    limit_requests=kw['limit_requests'],
                    show_title=kw['show_title'],
                    start_time=kw['start_time'],
                    songs=new_songs, current_page='artist', listeners=kw['listeners'],)