# encoding: utf-8

from __future__ import print_function, unicode_literals

def ready(sessionmaker):
    print("Starting the bmillham session ready")
    global session
    session = sessionmaker
