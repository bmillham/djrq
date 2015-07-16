import djrq.middleware
import web
from djrq.model import get_new_pending_requests_info, get_artist_by_letter
from djrq.model import get_artist_letters_counts, get_album_by_letter, get_album_letters_counts
from basecontroller import BaseController
from urllib2 import unquote

class BrowseController(BaseController):
    def __before__(self, *args, **kw):
        if args:
            try: # Needed because paster handles URLs different than nginx 
                letter = unicode(unquote(str(args[0])), "utf8")
            except UnicodeError, e: # If it's a unicode error, we are running under paster so just use what we got
                letter = args[0]
            if letter == '.dot': letter = '.'
            args = (letter, ) + args[1:]  # Inject it back.

        return super(BrowseController, self).__before__(*args, **kw)
    
    def __after__(self, result, *args, **kw):
        result, kw = result
        result = ('djrq.templates.letters', dict(result,  # Extend what the individual controller returns.
                #letter = args[0] if args else None,
                #browseletter = result['letter'],
                requests_count = kw['requests_count'],
                listeners=kw['listeners'],
                #requests_count = get_new_pending_requests_info()[0],
            ))
        return super(BrowseController, self).__after__(result, *args, **kw)
    
    def artist(self, letter=None, **kw):
        browse_by = "artist"
        a_list = get_artist_by_letter(kw['selected_catalogs'], letter) if letter else None
        letters=get_artist_letters_counts(kw['selected_catalogs'])
        return dict(letters=letters,
                    a_list=a_list,
                    browse_by='artist',
                    browseletter=letter,
                    ), kw
    
    def album(self, letter=None, **kw):
        browse_by = 'album'
        a_list = get_album_by_letter(kw['selected_catalogs'], letter) if letter else None
        return dict(letters=get_album_letters_counts(kw['selected_catalogs']), a_list=a_list, browse_by='album', browseletter=letter), kw