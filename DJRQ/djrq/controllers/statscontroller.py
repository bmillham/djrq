import djrq.middleware
import web
from ..model import session, func
from ..model.helpers import *
from ..model.played import Played
from ..model.song import Song
from basecontroller import BaseController

class StatsController(BaseController):
    def index(self, *args, **kwargs):
        catalogs = kwargs['selected_catalogs']
        played_by_me = get_played_by_me(catalogs)
        total_artists = get_total_artists(catalogs)
        total_albums = get_total_albums(catalogs)
        stats = get_song_stats(catalogs)
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
                                                  limit_requests=kwargs['limit_requests'],
                                                  show_title=kwargs['show_title'],
                                                  start_time=kwargs['start_time'],
                                                  topartists=topartists,
                                                  mostrequested=mostrequested,
                                                  toprequestors=toprequestors)
