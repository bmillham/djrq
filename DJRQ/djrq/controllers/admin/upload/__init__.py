from ...basecontroller import BaseController
from forms.privateform import PrivateForm
from forms.sharedform import SharedForm
from ..account import AccountMixIn

class UploadController(BaseController, AccountMixIn):
    private = PrivateForm()
    shared = SharedForm()
