import djrq.middleware
import web
from ...model import session
from ...model.helpers import get_all_requests_info, get_new_pending_requests_info
from ...model.requestlist import RequestList
from ..basecontroller import BaseController
from web.auth import authorize
from account import AccountMixIn

class RequestsController(BaseController, AccountMixIn):
    def __before__(self, *args, **kw):
        if len(args) > 1:
            change = (session.query(RequestList).filter(RequestList.id == args[0]).one(), args[1])
        else:
            change = None
        kw['change'] = change
        if 'request_view' not in web.core.session:
            web.core.session['request_view'] = ['np']
        return super(RequestsController, self).__before__(*args, **kw)
        

    def __after__(self, *args, **kw):
        if web.core.session['request_view'][0] == 'np':
            view = ['new', 'pending']
        else:
            view = web.core.session['request_view']
        print "View", view
        requests = session.query(RequestList).filter(RequestList.status.in_(view)).order_by(RequestList.t_stamp.desc())
        try:
            temp, rkw = args[0]
        except:
            temp = 'djrq.templates.admin.request_list'
            rkw = args[0]
        rkw['all_requests'] = dict()
        for stat in get_all_requests_info():
            print stat.status, stat.request_count, stat.request_length
            rkw['all_requests'][stat.status] = dict(request_count=stat.request_count, request_length=stat.request_length)
        empty = dict(request_count=0, request_length=0)
        for stat in ('new', 'pending', 'played', 'ignored'):
            if stat not in rkw['all_requests']:
                rkw['all_requests'][stat] = empty
        rkw['all_requests']['np'] = dict(request_count=rkw['requests_count'], request_length=rkw['requests_length'])
        return super(RequestsController, self).__after__((temp,
                                                             dict(rkw,
                                                                  requests=requests,
                                                                  )))

    @authorize(web.auth.authenticated)
    def index(self, *args, **kw):
        return kw

    @authorize(web.auth.authenticated)
    def change_status(self, *args, **kw):
        item, status = kw['change']
        if status == 'delete':
            session.delete(item)
            session.flush()
            kw['requests_count'], kw['requests_length'] = get_new_pending_requests_info()
        else:
            item.status = status
            session.add(item)
        return kw

    @authorize(web.auth.authenticated)
    def change_view(self, *args, **kw):
        web.core.session['request_view'] = [args[0]]
        return kw