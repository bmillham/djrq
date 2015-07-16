import djrq.middleware
import web
from djrq.model import *
from basecontroller import BaseController

class StatsController(BaseController):
    def index(self, *args, **kwargs):
        catalogs = kwargs['selected_catalogs']
        played_by_me = session.query(func.count(Played.track_id.distinct()).label('total')).join(Song).filter(Song.catalog.in_(catalogs), Played.played_by_me == 1).one()
        total_artists = session.query(func.count(Artist.fullname.distinct()).label('total')).join(Song).filter(Song.catalog.in_(catalogs)).one()
        total_albums = session.query(func.count(Album.id.distinct()).label('total')).join(Song).filter(Song.catalog.in_(catalogs)).one()
        stats = session.query(func.sum(Song.size).label('song_size'),
                              func.count(Song.id).label('total_songs'),
                              func.avg(Song.size).label('avg_song_size'),
                              func.sum(Song.time).label('song_time'),
                              func.avg(Song.time).label('avg_song_time')).filter(Song.catalog.in_(catalogs)).one()
        top_10 = get_top_10(catalogs)
        topartists = get_top_played_by_me(catalogs)
        mostrequested = get_top_requested(catalogs)
        toprequestors = get_top_requestors(catalogs)
        return "djrq.templates.stats", dict(stats=stats,
                                            listeners=kwargs['listeners'],
                                                  top_10=top_10,
                                                  played_by_me = played_by_me,
                                                  total_artists = total_artists,
                                                  total_albums = total_albums,
                                                  current_page="stats",
                                                  requests_count=kwargs['requests_count'],
                                                  topartists=topartists,
                                                  mostrequested=mostrequested,
                                                  toprequestors=toprequestors)
