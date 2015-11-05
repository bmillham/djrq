from web.core import request
import djrq.middleware
import web
#from djrq.model import *
from ..model.helpers import get_last_played

from basecontroller import BaseController

class RootController(BaseController):
    from requestcontroller import RequestController
    from whatsnewcontroller import WhatsNewController
    from browsecontroller import BrowseController
    from artistcontroller import ArtistController
    from albumcontroller import AlbumController
    from statscontroller import StatsController
    from siteoptionscontroller import SiteOptionsController
    from forms.searchform import SearchForm
    from forms.mistagform import MistagForm
    from forms.requestform import RequestForm
    from forms.suggestionform import SuggestionForm
    from forms.advancedsearchform import AdvancedSearchForm

    search = SearchForm()
    advancedsearch = AdvancedSearchForm()
    requestform = RequestForm()
    mistagform = MistagForm()
    suggestion = SuggestionForm()
    requests = RequestController()
    whatsnew = WhatsNewController()
    browse = BrowseController()
    artist = ArtistController()
    album = AlbumController()
    stats = StatsController()
    siteoptions = SiteOptionsController()

    #def __before__(self, *args, **kwargs):
    #    session = request.environ['dbsession']
    #    kwargs['requests_count'], kwargs['requests_length'] = get_new_pending_requests_info()
    #    #kwargs['selected_catalogs'] = [1,4]
    #    print "In root before, setting args", args, kwargs
    #    if 'nick' not in web.core.session:
    #        web.core.session['nick'] = ""
    #    return super(RootController, self).__before__(*args, **kwargs)


    def index(self, *args, **kwargs):
        last_played = get_last_played(kwargs['selected_catalogs'])
        return 'djrq/templates/lastplayed.html', {'last_played': last_played,
                                                  'current_page': "last_played",
                                                  'listeners': kwargs['listeners'],
                                                  'show_title': kwargs['show_title'],
                                                  'start_time': kwargs['start_time'],
                                                  'limit_requests': kwargs['limit_requests'],
                                                  'requests_count': kwargs['requests_count']}

