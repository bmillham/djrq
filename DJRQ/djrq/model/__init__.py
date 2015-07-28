from paste.registry import StackedObjectProxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy import *
from sqlalchemy.sql import func, or_
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_fulltext import FullText, FullTextSearch
from time import time
import markupsafe
import paste
from web.core import request

Base = declarative_base()
metadata = Base.metadata
session = StackedObjectProxy()

"""from artist import Artist
from album import Album
from played import Played
from requestlist import RequestList
from song import Song"""

class Album(Base):
    __tablename__ = 'album'
    __fulltext_columns__ = ('name',)
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    prefix = Column(String(32))
    year = Column(Integer)
    disk = Column(SmallInteger)
    Index(name)
    Index(prefix)
    __table_args__ = {'mysql_engine':'MyISAM'}

    def __unicode__(self):
        return u'<a href="/album/id/{}">{}</a>'.format(self.id, self.fullname)

    def get_url(self):
        return "/album/{}".format(self.id)

    @hybrid_property
    def fullname(self):
        if self.prefix is None:
            return self.name
        else:
            return self.prefix + " " + self.name

    @fullname.expression
    def fullname(self):
        return func.concat_ws(" ", self.prefix, self.name)

class Artist(Base):
    __tablename__ = 'artist'
    __fulltext_columns__ = ('name',)
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    prefix = Column(String(32))
    Index(name)
    Index(prefix)
    
    __table_args__ = {'mysql_engine':'MyISAM'}
    #def __repr__(self):
    #    return "{} |||| {} |||| {}".format(self.id, self.fullname, 'artist')

    def __unicode__(self):
        return u'<a href="/artist/id/{}">{}</a>'.format(self.id, self.fullname)

    def get_url(self):
        return "/artist/{}".format(self.id)

    @hybrid_property
    def fullname(self):
        if self.prefix is None:
            return self.name
        else:
            return self.prefix + " " + self.name

    @fullname.expression
    def fullname(self):
        return func.concat_ws(" ", self.prefix, self.name)

class Mistags(Base):
    __tablename__ = 'mistags'
    __table_args__ = {'mysql_engine':'MyISAM'}
    id = Column(Integer, primary_key=True)
    track_id = Column(Integer, ForeignKey('song.id'))
    reported_by = Column(String(255))
    reported = Column(TIMESTAMP)
    artist = Column(String(255))
    album = Column(String(255))
    title = Column(String(255))
    comments = Column(String(255))

class Played(Base):
    __tablename__ = 'played'
    __table_args__ = {'mysql_engine':'MyISAM'}
    played_id = Column(Integer, primary_key=True)
    track_id = Column(Integer, ForeignKey('song.id'))
    date_played = Column(DateTime)
    played_by = Column(String(255))
    played_by_me = Column(Integer)

    def get_multi_albums(self):
        return session.query(Song).join(Album).join(Artist).filter(Artist.fullname == self.song.artist.fullname, Song.title == self.song.title)

class RequestList(Base):
    __tablename__= 'requestlist'
    __table_args__ = {'mysql_engine':'MyISAM'}
    id = Column(Integer, primary_key=True)
    song_id = Column('songID', Integer, ForeignKey('song.id'))
    t_stamp = Column(DateTime)
    host = Column(String(255))
    msg = Column(String(255))
    name = Column(String(255))
    code = Column(Integer)
    eta = Column('ETA', DateTime)
    status = Column(Enum('played', 'ignored', 'pending', 'new'))

class Song(Base):
    __tablename__ = 'song'
    __fulltext_columns__ = ('title,')

    id = Column(Integer, primary_key=True)
    file = Column(String(512))
    catalog = Column(Integer)
    album_id  = Column("album", Integer, ForeignKey('album.id'))
    year = Column(Integer)
    artist_id = Column("artist", Integer, ForeignKey('artist.id'))
    title = Column(String(255))
    size = Column(Integer)
    time = Column(SmallInteger)
    track = Column(SmallInteger)
    #was_played = Column('played', SmallInteger)
    addition_time = Column(Integer)
    __table_args__ = {'mysql_engine':'MyISAM'}
    album = relationship("Album", backref=backref('songs', order_by=track))
    artist = relationship("Artist", backref=backref('songs', order_by=title))
    played = relationship("Played", backref=backref('song'), order_by=Played.date_played.desc())
    requests = relationship("RequestList", backref=backref('song'), order_by=RequestList.t_stamp.desc())
    played_requests = relationship("RequestList",
                                   primaryjoin="and_(RequestList.song_id==Song.id, RequestList.status == 'played')",
                                   order_by=RequestList.t_stamp.desc())
    new_requests = relationship("RequestList", 
                                primaryjoin="and_(RequestList.song_id==Song.id, or_(RequestList.status == 'new', RequestList.status=='pending'))")
    mistags = relationship("Mistags", backref=backref('song'))

class Suggestions(Base):
    __tablename__ = 'suggestions'
    __table_args__ = {'mysql_engine':'MyISAM'}
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    album = Column(String(255))
    artist = Column(String(255))
    suggestor = Column(String(255))
    comments = Column(String(255))

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    fullname = Column(String(255))
    email = Column(String(255))
    website = Column(String(255))
    apikey = Column(String(255))
    password = Column(String(64))
    access = Column(Integer())
    disabled = Column(Integer())
    last_seen = Column(Integer())
    create_date = Column(Integer())
    validation = Column(String(255))

class SiteOptions(Base):
    __tablename__ = "site_options"
    id = Column(Integer, primary_key=True)
    show_title = Column(String(255))
    show_time = Column(String(255))
    show_end = Column(String(255))
    limit_requests = Column(String(255))
    offset = Column(Integer)
    catalog = Column(String(255))

class Listeners(Base):
    __tablename__ = "listeners"
    id = Column(Integer, primary_key=True)
    current = Column(Integer)
    max = Column(Integer)

#def ready(sessionmaker):
#    global session
#    session = sessionmaker
#    request.environ['catalogs'] = session.query(SiteOptions).limit(1).one()

def get_new_pending_requests_info():
    return session.query(func.count(RequestList.id).label('request_count'),
                  func.sum(Song.time).label('request_length')).\
                  join(Song).filter(or_(RequestList.status=="new", RequestList.status=='pending')).one()

def get_last_played(catalogs, limit=50):
    return session.query(func.count(Played.date_played), func.avg(Song.time), Played).join(Song).filter(Song.catalog.in_(catalogs)).group_by(Played.date_played).order_by(Played.date_played.desc()).limit(limit)

def get_multi_ablums(artist_name, song_title):
    return session.query(Song).join(Album).join(Artist).filter(Artist.fullname == artist_name, Song.title == song_title)

def get_artist_letters_counts(catalogs):
    return session.query(func.left(Artist.name, 1), func.count(Artist.id.distinct())).join(Song).filter(Song.catalog.in_(catalogs)).group_by(func.left(Artist.name, 1))

def get_album_letters_counts(catalogs):
    return session.query(func.left(Album.name, 1), func.count(Album.id.distinct())).join(Song).filter(Song.catalog.in_(catalogs)).group_by(func.left(Album.name, 1))

def get_new_artists(catalogs, start_time):
    return session.query(func.count(Song.artist_id), func.sum(Song.time), func.sum(Song.size), Song).filter(Song.addition_time >= start_time, Song.catalog.in_(catalogs)).order_by(Song.addition_time.desc()).group_by(Song.artist_id)

def get_new_counts(catalogs, start_time):
    return session.query(func.count(Song.id), func.sum(Song.time), func.sum(Song.size)).filter(Song.addition_time >= start_time, Song.catalog.in_(catalogs)).one()

def get_artist_by_letter(catalogs, letter):
    return session.query(Artist).join(Song).filter(Artist.name.startswith(letter), Song.catalog.in_(catalogs)).order_by(Artist.name).group_by(Artist.id)

def get_album_by_letter(catalogs, letter):
    return session.query(Album).join(Song).filter(Album.name.startswith(letter), Song.catalog.in_(catalogs)).order_by(Album.name).group_by(Album.id)

def get_top_10(catalogs):
    return session.query(func.count(Song.artist_id).label('artist_count'),
                         Song.artist_id,
                         Artist.fullname.label('artist_fullname')).join(Artist).filter(Song.catalog.in_(catalogs)).group_by(Song.artist_id).order_by(func.count(Song.artist_id).desc()).limit(10)

def get_top_played_by_me(catalogs):
    return  session.query(Played,
                          func.count(Played.track_id).label('played_count'),
                          func.max(Played.date_played).label('date_played')).join(Song).filter(Song.catalog.in_(catalogs), Played.played_by_me == 1).group_by(Played.track_id).order_by(func.count(Played.track_id).desc()).limit(10)

def get_top_played_by_all(catalogs):
    return session.query(func.count(Played.track_id), Song, func.max(Played.date_played)).join(Song).filter(Song.catalog.in_(catalogs)).group_by(Played.track_id).order_by(func.count(Played.track_id).desc()).limit(10)
    
def get_top_requested(catalogs):
    return session.query(Song).\
                         join(RequestList).\
                         filter(Song.catalog.in_(catalogs), RequestList.status == 'played').\
                         group_by(RequestList.song_id).\
                         order_by(func.count(RequestList.song_id).desc()).limit(10)

def get_top_requestors(catalogs):
    return session.query(func.count(RequestList.name).label('request_count'),
                         RequestList.name.label('requestor'),
                         func.max(RequestList.t_stamp).label('last_request')).join(Song).filter(Song.catalog.in_(catalogs)).group_by(RequestList.name).order_by(func.count(RequestList.name).desc()).limit(10)

def full_text_search(catalogs, phrase):
    return session.query(Song).join(Artist).join(Album).filter(((Song.title.match(phrase)) | (Artist.name.match(phrase)) | (Album.name.match(phrase))), Song.catalog.in_(catalogs))

def advanced_search(catalogs, search_for, phrase):
    if search_for == 'title':
        search = Song.title
    elif search_for == 'artist':
        search = Artist.name
    elif search_for == 'album':
        search = Album.name
    return session.query(Song).join(Artist).join(Album).filter(search.like(phrase), Song.catalog.in_(catalogs))

def get_current_requests():
    return session.query(RequestList).\
                       filter((RequestList.status == 'new') | (RequestList.status == 'pending')).order_by(RequestList.id)
