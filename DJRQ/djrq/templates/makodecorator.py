# makodecorator.py
# License: None, public domain
# Version: 1.0.0
# Author: Robert Thomson - http://blog.corporatism.org/

from mako.lookup import TemplateLookup
from mako import exceptions
#import settings

import sys
import os.path
from web.core import HTTPMethod

# with thanks to Peter Hunt (http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/465427)
decorator_with_args = lambda decorator: lambda *args, **kwargs: lambda func: \
                      decorator(func, *args, **kwargs)

@decorator_with_args
def mako(func, template=None):
    def MAKOIFY(request, *args, **kwargs):
        res = func(request, *args, **kwargs)
        if not res:
            res = {}
        if type(res) == dict:
            # use current_app/mako_templates/ as first search path.
            # the assumption is that the function's module is under current_app/
            d = os.path.join(
                  os.path.dirname(sys.modules[func.__module__].__file__),
                  "mako_templates/")
            lookup = TemplateLookup(directories=[d, 'mako_templates/'])
            res['request'] = request
            try:
                t = lookup.get_template(template)
                return HTTPMethod(t.render(**res))
            except:
                #if settings.DEBUG:
                if True:
                    # display Mako's debug page on template error
                    return HTTPMethod(exceptions.html_error_template()\
                                        .render(), status=500)
                raise
        else:
            # if not a dictionary or empty value, return literal result
            return res
    MAKOIFY.__name__ = func.__name__
    MAKOIFY.__doc__ = func.__doc__
    MAKOIFY.__dict__ = func.__dict__
    return MAKOIFY

"""Example usage:
from makodecorator import mako

@mako("index.mako")
def foo(request, id):
        return { "name" : "Robert Thomson" }
"""
