import djrq.middleware
import web
from web.core.templating import render
from datetime import datetime
from ...model import session
from ...model.song import Song
from ...model.requestlist import RequestList

class RequestForm(web.core.HTTPMethod):
    def get(self, *args, **kwargs):
        row = session.query(Song).filter(Song.id==args[1]).first()
        mimetype, output = render('djrq.templates.forms.request_form',
                                  dict(row=row, requestor=web.core.session['nick']))
        fragments = dict(fragments={'.myform': output})
        return "json:", fragments

    def post(self, *args, **kwargs):
        id = kwargs["trackId"]
        now = datetime.now()
        new_row = RequestList(song_id=id,
                              t_stamp=now,
                              host='0.0.0.0',
                              msg=kwargs['inputComment'],
                              name=kwargs['inputNick'],
                              code=0,
                              eta=now,
                              status='new')
        session.add(new_row)
        web.core.session['nick'] = kwargs['inputNick']
        request_count = kwargs['requests_count'] + 1
        fragments = dict(fragments={"#rb_text_%s" % id: "Requested",
                                    "datecontent": "requested",
                                    "#request_count": "<span class='badge' id='request_count'>%s</span>" % request_count})
        return "json:", fragments