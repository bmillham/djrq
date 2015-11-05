import djrq.middleware
import web
from web.core.templating import render
from datetime import datetime
from ...model import session
from ...model.mistags import Mistags
from ...model.song import Song

class MistagForm(web.core.HTTPMethod):
    def get(self, *args, **kwargs):
        row = session.query(Song).filter(Song.id==args[1]).first()
        mimetype, output = render('djrq.templates.forms.mistag_form', dict(row=row))
        fragments = dict(fragments={'.myform': output})
        return "json:", fragments

    def post(self, **kwargs):
        web.core.session['nick'] = kwargs['inputNick']
        fragments = {}
        new_row = Mistags(track_id=kwargs['trackId'],
                   reported=datetime.now(),
                   reported_by=kwargs['inputNick'],
                   comments=kwargs['inputComment'],
                   title=kwargs['inputTitle'],
                   artist=kwargs['inputArtist'],
                   album=kwargs['inputAlbum'])
        session.add(new_row)
        response = {}
        response['responseText'] = "Mistag<br/>Reported"
        response['fragments'] = dict({"#mb_text_%s" % id: "Reported"}),
        response['datacontent'] = "Reported By: %s" % kwargs['inputNick']
        fragments = dict(fragments={"#mb_text_%s" % id: "Reported",
                                    "datacontent": "Reported",
                                    })
        #response['mb_' % kwargs['trackId']]
        return 'json:', response