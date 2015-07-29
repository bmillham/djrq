from ...basecontroller import BaseController
from forms.catalogform import CatalogForm
from forms.showinfoform import ShowInfoForm

class OptionsController(BaseController):
    catalog = CatalogForm()
    showinfo = ShowInfoForm()