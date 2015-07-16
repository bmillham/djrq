# encoding: utf-8
 
from web.core import request
from web.core.middleware import middleware
 
# Don't actually try importing "engine" or "metadata" or "session" yet.
from djrq import model
from djrq import bmillham
from djrq import overflow

@middleware('domain', after=['database'])
def domain(app, config):
	"""Perform any request setup that differs on a per-domain basis."""
	
	# This function is run once on startup.
	
	# This is a low-level "WSGI middleware" layer.  It runs the actual app on each request.
	def domain_inner(environ, start_response):
		try:
			dj_name = environ['HTTP_HOST'].split(".")[0]
		except:
			dj_name = 'default'
		print "Domain will be:", dj_name
		if dj_name == 'bmillham':
			environ['dbsession'] = bmillham.session
		elif dj_name == 'overflow':
			environ['dbsession'] = overflow.session
		else:
			environ['dbsession'] = bmillham.session
			environ['dbmodel'] = bmillham
		environ['mytest'] = 'test'
		# Get desired catalogs


		return app(environ, start_response)
	
	# And the web server runs what we return here.
	return domain_inner