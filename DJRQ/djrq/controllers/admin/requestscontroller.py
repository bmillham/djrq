import djrq.middleware
import web
from djrq.model import *
from ..basecontroller import BaseController

class RequestsController(BaseController):
    def __before__(self, *args, **kw):
        if len(args) > 1:
            change = (session.query(RequestList).filter(RequestList.id == args[0]).one(), args[1])
        else:
            change = None
        kw['change'] = change
        if 'request_view' not in web.core.session:
            web.core.session['request_view'] = 'np'
        return super(RequestsController, self).__before__(*args, **kw)
        

    def __after__(self, rkw, *args, **kw):
        print rkw, args, kw
        if web.core.session['request_view'][0] == 'np':
            view = ['new', 'pending']
        else:
            view = web.core.session['request_view']
        print "View", view
        requests = session.query(RequestList).filter(RequestList.status.in_(view)).order_by(RequestList.t_stamp.desc())
        rkw['all_requests'] = dict()
        for stat in get_all_requests_info():
            print stat.status, stat.request_count, stat.request_length
            #kw['all_requests'][stat.status] = dict()
            rkw['all_requests'][stat.status] = dict(request_count=stat.request_count, request_length=stat.request_length)
        empty = dict(request_count=0, request_length=0)
        for stat in ('new', 'pending', 'played', 'ignored'):
            if stat not in rkw['all_requests']:
                rkw['all_requests'][stat] = empty
        rkw['all_requests']['np'] = dict(request_count=rkw['requests_count'], request_length=rkw['requests_length'])
        return super(RequestsController, self).__after__(('djrq.templates.admin.request_list', 
                                                             dict(rkw,
                                                                  requests=requests,
                                                                  )))

    def index(self, *args, **kw):
        return kw

    def change_status(self, *args, **kw):
        item, status = kw['change']
        print "Change status to", status
        if status == 'delete':
            #delmistag = session.query(Mistags).filter(Mistags.id==args[0]).one()
            #session.autoflush = False
            session.delete(item)
            session.flush()
            kw['requests_count'], kw['requests_length'] = get_new_pending_requests_info()
            #session.autoflush = True
        else:
            item.status = status
            session.add(item)
        return kw

    def change_view(self, *args, **kw):
        web.core.session['request_view'] = [args[0]]
        return kw

    #def new(self, *args, **kw):
    #    kw['rq_up'].status = 'new'
    #    session.add(kw['rq_up'])
    #    return kw

    #def pending(self, *args, **kw):
    #    kw['rq_up'].status = 'pending'
    #    session.add(kw['rq_up'])
    #    return kw

    #def delete(self, *args, **kw):
        #delmistag = session.query(Mistags).filter(Mistags.id==args[0]).one()
        #session.delete(delmistag)
    #    return kw
