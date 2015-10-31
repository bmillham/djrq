import djrq.middleware
import web
from djrq.model import get_current_requests, get_new_pending_requests_info, get_new_artists, get_new_counts
from time import time
from basecontroller import BaseController

class WhatsNewController(BaseController):
    def index(self, *args, **kwargs):
        start_time = time() - (60 * 60 * 24 * 90) # 7 days
        wn = get_new_artists(kwargs['selected_catalogs'], start_time)
        wn_stats = get_new_counts(kwargs['selected_catalogs'], start_time)
        return 'djrq.templates.whatsnew', dict(
                                               requests_count=kwargs['requests_count'],
                                               requests_length=kwargs['requests_length'],
                                               listeners=kwargs['listeners'],
                                               whatsnew=wn,
                                               new_start_time=start_time,
                                               whatsnew_stats=wn_stats,
                                               limit_requests=kwargs['limit_requests'],
                                               show_title=kwargs['show_title'],
                                               start_time=kwargs['start_time'],
                                              )