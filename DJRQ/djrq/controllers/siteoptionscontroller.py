import djrq.middleware
import web
from ..model import session
from ..model.listeners import Listeners
from ..model.helpers import get_current_requests, get_new_artists, get_new_counts
from ..model.helpers import get_new_pending_requests_info
from time import time
from basecontroller import BaseController

class SiteOptionsController(web.core.HTTPMethod):
    def __after__(self, result, *args, **kw):
        themes = ('bootstrap', 'cerulean', 'cosmo', 'cyborg', 'darkly', 'flatly', 'journal', 
                  'lumen', 'paper', 'sandstone', 'simplex', 'slate', 'spacelab', 'superhero',
                  'united', 'yeti')
        if 'theme' in web.core.session:
            current_theme = web.core.session['theme']
        else:
            current_theme='cerulean'
        if 'nolettercounts' in web.core.session:
            nolettercounts = web.core.session['nolettercounts']
        else:
            nolettercounts = False
 
        result = ('djrq.templates.siteoptions', dict(result,  # Extend what the individual controller returns.
                requests_count=kw['requests_count'],
                show_title=kw['show_title'],
                start_time=kw['start_time'],
                themes=themes,
                current_theme=current_theme,
                nolettercounts=nolettercounts,
                listeners=kw['listeners'],
            ))
        return super(SiteOptionsController, self).__after__(result, *args, **kw)

    def get(self, *args, **kwargs):
        return dict(settings_saved=False)

    def post(self, *args, **kwargs):
        web.core.session['theme'] = kwargs['theme']
        if 'lettercheck' in kwargs:
            web.core.session['nolettercounts'] = True
        else:
            web.core.session['nolettercounts'] = False
        return dict(settings_saved=True)
    