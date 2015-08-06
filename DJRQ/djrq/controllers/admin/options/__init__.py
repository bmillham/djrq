from ...basecontroller import BaseController
from forms.catalogform import CatalogForm
from forms.showinfoform import ShowInfoForm
from forms.requestform import RequestForm
from ..account import AccountMixIn

class OptionsController(BaseController, AccountMixIn):
    catalog = CatalogForm()
    showinfo = ShowInfoForm()
    requests = RequestForm()