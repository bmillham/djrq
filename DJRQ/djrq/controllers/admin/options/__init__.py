from ...basecontroller import BaseController
from forms.catalogform import CatalogForm
from forms.showinfoform import ShowInfoForm
from forms.requestform import RequestForm

class OptionsController(BaseController):
    catalog = CatalogForm()
    showinfo = ShowInfoForm()
    requests = RequestForm()