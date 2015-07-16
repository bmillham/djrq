from web.core import request
import djrq.middleware
import web
from web.core.templating import render
from djrq.model import *

class SuggestionForm(web.core.HTTPMethod):
    def post(self, **kwargs):
        web.core.session['nick'] = kwargs['inputNick']
        new_row = Suggestions(suggestor=kwargs['inputNick'],
                        artist=kwargs['inputArtist'],
                        album=kwargs['inputAlbum'],
                        title=kwargs['inputTitle'],
                        comments=kwargs['inputComment']
                        )
        session.add(new_row)
        return