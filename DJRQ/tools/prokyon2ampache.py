from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, SmallInteger, Time, DateTime, Enum
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, joinedload, subqueryload, contains_eager
from sqlalchemy.sql import func, or_
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils.functions import create_database, database_exists
from time import time
from datetime import datetime
from tools.model import prokyon
from djrq import model as ampache
import os
import sys

tables_needed = False
print "Connecting to the database"

Base = declarative_base()
ampache_engine = create_engine('mysql+oursql://sqlalchemy:password@localhost/thefranswer_ampache?charset=utf8', echo=False, encoding='utf8')
prokyon_engine = create_engine('mysql+oursql://sqlalchemy:password@localhost/thefranswer?charset=utf8', echo=False, encoding='utf8')
if not database_exists('mysql+oursql://sqlalchemy:password@localhost/thefranswer_ampache'):
    create_database('mysql+oursql://sqlalchemy:password@localhost/thefranswer_ampache')
    tables_needed = True

Session = sessionmaker(binds={ampache.Song: ampache_engine,
                              ampache.Artist: ampache_engine,
                              ampache.Album: ampache_engine,
                              ampache.RequestList: ampache_engine,
                              ampache.Mistags: ampache_engine,
                              ampache.Played: ampache_engine,
                              ampache.Suggestions: ampache_engine,
                              ampache.User: ampache_engine,
                              ampache.SiteOptions: ampache_engine,
                              ampache.Listeners: ampache_engine,
                              prokyon.Tracks: prokyon_engine,
                              prokyon.RequestList: prokyon_engine,
                              prokyon.Mistags: prokyon_engine,
                              prokyon.Played: prokyon_engine,
                              prokyon.Suggestions: prokyon_engine,
                              prokyon.User: prokyon_engine,
                              prokyon.SiteOptions: prokyon_engine,
                              prokyon.Listeners: prokyon_engine})
session = Session()

if tables_needed:
    ampache.Artist().__table__.create(ampache_engine)
    ampache.Album().__table__.create(ampache_engine)
    ampache.Song().__table__.create(ampache_engine)
    ampache.RequestList().__table__.create(ampache_engine)
    ampache.Mistags().__table__.create(ampache_engine)
    ampache.Played().__table__.create(ampache_engine)
    ampache.Suggestions().__table__.create(ampache_engine)
    ampache.User().__table__.create(ampache_engine)
    ampache.SiteOptions().__table__.create(ampache_engine)
    ampache.Listeners().__table__.create(ampache_engine)
    ft = "ALTER TABLE :table ADD FULLTEXT idjc (:column)"
    session.execute("ALTER TABLE artist ADD FULLTEXT idjc (name)", mapper=ampache.Artist)
    session.execute("ALTER TABLE album ADD FULLTEXT idjc (name)", mapper=ampache.Album)
    session.execute("ALTER TABLE song ADD FULLTEXT idjc (title)", mapper=ampache.Song)

def get_prefix(fullname):
    fullname = fullname.strip()
    if fullname is None:
        fullname = "[UNKNOWN]"
    if fullname.lower().startswith('the '):
        prefix, name = fullname.split(' ', 1)
    else:
        prefix = None
        name = fullname
    return fullname.lower(), prefix, name

print "Copying Suggestions"
max_id = session.query(func.max_(ampache.Suggestions.id)).one()[0]
if max_id is None:
    max_id = 0
print "Max id", max_id
for s in session.query(prokyon.Suggestions).filter(prokyon.Suggestions.id > max_id).order_by(prokyon.Suggestions.id):
    sg = ampache.Suggestions(id=s.id, title=s.title, artist=s.artist, album=s.album, suggestor=s.suggestor,
                             comments=s.comments)
    session.add(sg)
print "Commiting suggestions"
session.commit()
print "Copying User"
#max_id = session.query(prokyon.User).one()
for u in session.query(prokyon.User):
    try:
        uq = session.query(ampache.User).filter(ampache.User.username==u.username).one()
    except:
        user = ampache.User(username=u.username, password=u.password)
        session.add(user)
print "Commiting User"
session.commit()
print "Copying Site Options"
max_id = session.query(func.max_(ampache.SiteOptions.id)).one()[0]
if max_id is None: max_id = 0
print "max_id", max_id
for s in session.query(prokyon.SiteOptions).filter(prokyon.SiteOptions.id > max_id).order_by(prokyon.SiteOptions.id):
    so = ampache.SiteOptions(id=s.id, show_title=s.show_title, show_time=s.show_time, show_end=s.show_end,
                             limit_requests=s.limit_requests, offset=s.offset, catalog="0")
    session.add(so)
print "Commiting Site Options"
session.commit()
print "Copying Listeners"
max_id = session.query(func.max_(ampache.Listeners.id)).one()[0]
if max_id is None: max_id = 0
for l in session.query(prokyon.Listeners).filter(prokyon.Listeners.id > max_id).order_by(prokyon.Listeners.id):
    ls = ampache.Listeners(id=l.id, current=l.current, max=l.max)
    session.add(ls)
print "Commiting Listeners"
session.commit()

found_artists = {}
found_albums = {}

print "Getting tracks"
max_id = session.query(func.max_(ampache.Song.id)).one()[0]
if max_id is None: max_id = 0
count = 0
tracks = session.query(prokyon.Tracks).filter(prokyon.Tracks.id > max_id).order_by(prokyon.Tracks.id)
print "Adding tracks to new database"
total = tracks.count()
for t in tracks:
    #print "Checking track", t.title, t.artist, t.album, t.path, t.filename
    count += 1
    fullfilename = os.path.join(t.path, t.filename)
    art_fullname, art_prefix, art_name = get_prefix(t.artist)
    try:
        artist = found_artists[art_fullname]
    except:
        try:
            artist = session.query(ampache.Artist).filter(ampache.Artist.name==art_name, ampache.Artist.prefix==art_prefix).one()
        except:
            print "Adding new artist", t.artist
            artist = ampache.Artist(prefix=art_prefix, name=art_name)
            session.add(artist)
        found_artists[art_fullname] = artist
    alb_fullname, alb_prefix, alb_name = get_prefix(t.album)
    try:
        album = found_albums[alb_fullname]
    except:
        try:
            album = session.query(ampache.Album).filter(ampache.Album.name==alb_name, ampache.Artist.prefix==alb_prefix).one()
        except:
            print "Adding new Album", t.album
            album = ampache.Album(prefix=alb_prefix, name=alb_name)
            session.add(album)
        found_albums[alb_fullname] = album
    
    requests = []
    if len(t.requests) > 0:
        for r in t.requests:
            requests.append(ampache.RequestList(t_stamp=r.t_stamp, host=r.host, msg=r.msg, name=r.name, code=r.code, eta=r.eta, status=r.status))
    
    mistags = []
    if len(t.mistags) > 0:
        for m in t.mistags:
            mistags.append(ampache.Mistags(reported_by=m.reported_by, reported=m.reported, artist=m.artist,
                                           album=m.album, title=m.title, comments=m.comments))
    
    played = []
    if len(t.played):
        for p in t.played:
            played.append(ampache.Played(date_played=p.date_played, played_by=p.played_by,
                                         played_by_me=p.played_by_me))
    
    if t.lastModified is not None:
        addition_time = datetime.strptime(str(t.lastModified), "%Y-%m-%d %H:%M:%S").strftime("%s")
    else:
        addition_time = None
    s = ampache.Song(id=t.id, title=t.title, artist=artist, album=album, file=fullfilename,
                     time=t.length, catalog=t.jingle, size=t.size, track=t.tracknumber, addition_time=addition_time,
                     requests=requests, mistags=mistags, played=played)
    
    session.add(s)
    if count % 100 == 0:
        print "------------------Commiting %s of %s (%s)------------------" % (count, total, t.id)
        session.commit()
session.commit() # Get the last tracks added