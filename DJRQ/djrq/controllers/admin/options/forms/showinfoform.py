import djrq.middleware
import web
from djrq.model import *
from web.auth import authorize

class ShowInfoForm(web.core.HTTPMethod):
    def __before__(self, *args, **kw):
        options = session.query(SiteOptions).one()
        kw['options'] = options
        kw['show_title'] = options.show_title
        kw['show_time'] = options.show_time
        kw['show_end'] = options.show_end
        return super(ShowInfoForm, self).__before__(*args, **kw)

    def __after__(self, result, *args, **kw):
        if type(result) == tuple:
            temp, result = result
        else:
            temp = 'djrq.templates.admin.options.forms.showinfo'
            kw.update(result)
        return super(ShowInfoForm, self).__after__((temp, kw))

    @authorize(web.auth.authenticated)
    def get(self, *args, **kw):
        return dict(status=None)

    @authorize(web.auth.authenticated)
    def post(self, *args, **kw):
        result = dict(status=None)
        if 'showtitlefield' in kw:
            if kw['options'].show_title != kw['showtitlefield']:
                kw['options'].show_title = kw['showtitlefield']
                result['show_title'] = kw['showtitlefield']
                result['status'] = "[Updated]"
        if 'showstartfield' in kw:
            if kw['options'].show_time != kw['showstartfield']:
                kw['options'].show_time = kw['showstartfield']
                result['show_time'] = kw['showstartfield']
                result['status'] = '[Updated]'
        if result['status'] is not None: session.commit()
        return result