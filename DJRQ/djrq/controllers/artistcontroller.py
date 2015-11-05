import djrq.middleware
import web
from ..model import session
from ..model.helpers import get_artist_letters_counts, get_new_pending_requests_info
from ..model.song import Song
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
                    viewing_new=False,
                    limit_requests=kw['limit_requests'],
                    show_title=kw['show_title'],
                    start_time=kw['start_time'],
                    songs=a.songs, current_page="artist", listeners=kw['listeners'],)

    def name(self, *args, **kw):
        fn = u'/'.join(args)
        s = session.query(Song).filter(Song.artist_fullname==fn).order_by(Song.title)
        return dict(artist=s[0].artist,
                    viewing_new=False,
                    limit_requests=kw['limit_requests'],
                    show_title=kw['show_title'],
                    start_time=kw['start_time'],
                    songs=s, current_page="artist", listeners=kw['listeners'],)

    def _newname(self, *args, **kw):
        from datetime import datetime, timedelta
        args = args[0]
        try:
            a = args.pop()
            days = int(a)
        except:
            days = 300
            args.append(a)
        name = u'/'.join(args)
        ago = datetime.now()-timedelta(days=days)
        new_songs = session.query(Song).filter(Song.artist_fullname==name, Song.addition_time>=ago).order_by(Song.title)
        try:
            a = new_songs[0].artist
        except:
            a = session.query(Song).filter(Song.artist_fullname==name).first().artist
        return a, new_songs

    def new(self, *args, **kw):
        args = list(args)
        arg = args.pop(0)
        if arg == 'name':
            a, new_songs = self._newname(args, **kw)
        else:
            id = int(arg)
            try:
                days = int(args[0])
            except:
                days = 30
            start = int(time()) - (60 * 60 * 24 * days)
            a = session.query(Artist).filter(Artist.id == id, Song.addition_time >= start).first()
            new_songs = session.query(Song).filter(Song.artist_id == id, Song.addition_time >= start).order_by(Song.title)
        return dict(artist=a,
                    viewing_new=True,
                    limit_requests=kw['limit_requests'],
                    show_title=kw['show_title'],
                    start_time=kw['start_time'],
                    songs=new_songs, current_page='artist', listeners=kw['listeners'],)