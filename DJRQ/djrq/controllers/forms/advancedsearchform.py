import web
from djrq.model import advanced_search

class AdvancedSearchForm(web.core.HTTPMethod):
    def get(self, *args, **kwargs):
        return 'djrq.templates.forms.advanced_search_form', dict(search_type=args[0],
                                                  requests_count=kwargs['requests_count'])

    def post(self, *args, **kwargs):
        f = advanced_search(kwargs['selected_catalogs'], kwargs['search_for'], kwargs['inputSearchText']) 
        requests_count = kwargs['requests_count']
        return('djrq.templates.searchresults', dict(searchresults=f,
                                                         requests_count=requests_count,
                                                         search_for=kwargs['search_for'],
                                                         listeners=kwargs['listeners'],
                                                         search_text=kwargs['inputSearchText']))