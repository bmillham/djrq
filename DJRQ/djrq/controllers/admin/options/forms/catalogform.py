import djrq.middleware
import web
from djrq.model import *
from web.auth import authorize
#from ...account import AccountMixIn

class CatalogForm(web.core.HTTPMethod):
    def __before__(self, *args, **kw):
        options = session.query(SiteOptions).one()
        kw['options'] = options
        kw['catalogs'] = session.query(Catalog)
        return super(CatalogForm, self).__before__(*args, **kw)

    def __after__(self, result, *args, **kw):
        kw.update(result)
        return super(CatalogForm, self).__after__(('djrq.templates.admin.catalog', kw))

    @authorize(web.auth.authenticated)
    def get(self, *args, **kw):
        return dict(status=None)

    @authorize(web.auth.authenticated)
    def post(self, *args, **kw):
        result = dict(status=None)
        if 'cat_group' in kw:
            cg = kw['cat_group']
            if type(cg) is not list:
                cg = [cg]
            cats = ",".join(cg)
            if kw['selected_catalogs'] == cg:
                result['status'] = "[No changes]"
            else:
                kw['selected_catalogs'] = cg
                kw['options'].catalog = cats
                session.commit()
                result['status'] = '[Updated]'
                result['selected_catalogs'] = cg
        return result