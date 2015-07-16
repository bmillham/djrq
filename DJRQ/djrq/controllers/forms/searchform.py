import web
from djrq.model import full_text_search

class SearchForm(web.core.HTTPMethod):
    def get(self, *args, **kwargs):
        return 'djrq.templates.forms.search_form', dict(search_type=args[0],
                                                  requests_count=kwargs['requests_count'])

    def post(self, *args, **kwargs):
        f = full_text_search(kwargs['selected_catalogs'], kwargs['search_text']) 
        requests_count = kwargs['requests_count']
        return('djrq.templates.searchresults', dict(searchresults=f,
                                                    search_for=None,
                                                    requests_count=requests_count,
                                                    listeners=kwargs['listeners'],
                                                    search_text=kwargs['search_text']))