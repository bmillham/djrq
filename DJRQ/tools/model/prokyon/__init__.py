from paste.registry import StackedObjectProxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy import *
from sqlalchemy.sql import func, or_
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.ext.hybrid import hybrid_property
from time import time
import markupsafe
import paste
from web.core import request


Base = declarative_base()
metadata = Base.metadata
session = StackedObjectProxy()

class Mistags(Base):
    __tablename__ = 'mistags'
    id = Column(Integer, primary_key=True)
    track_id = Column(Integer, ForeignKey('tracks.id'))
    reported_by = Column(String)
    reported = Column(TIMESTAMP)
    artist = Column(String)
    album = Column(String)
    title = Column(String)
    comments = Column(String)


class Played(Base):
    __tablename__ = 'played'
    played_id = Column(Integer, primary_key=True)
    track_id = Column(Integer, ForeignKey('tracks.id'))
    date_played = Column(DateTime)
    played_by = Column(String)
    played_by_me = Column(Integer)

    def get_multi_albums(self):
        return session.query(Song).join(Album).join(Artist).filter(Artist.fullname == self.song.artist.fullname, Song.title == self.song.title)

class RequestList(Base):
    __tablename__= 'requestlist'
    id = Column(Integer, primary_key=True)
    song_id = Column('songID', Integer, ForeignKey('tracks.id'))
    t_stamp = Column(DateTime)
    host = Column(String(255))
    msg = Column(String(255))
    name = Column(String(255))
    code = Column(Integer)
    eta = Column('ETA', DateTime)
    status = Column(Enum('played', 'ignored', 'pending', 'new'))

class Tracks(Base):
    __tablename__ = 'tracks'
    id = Column(Integer, primary_key=True)
    path = Column(String)
    filename = Column(String)
    artist = Column(String)
    album = Column(String)
    title = Column(String)
    size = Column(Integer)
    length = Column(Integer)
    tracknumber = Column(Integer)
    lastModified = Column(DateTime)
    jingle = Column(Integer)
    
    requests = relationship("RequestList", backref=backref('track'), order_by=RequestList.t_stamp.desc())
    played = relationship("Played", backref=backref('track'), order_by=Played.date_played.desc())
    mistags = relationship("Mistags", backref=backref('track'))

    @property
    def file(self):
        return "/".join((self.path, self.filename))

    @property
    def addition_time(self):
        return mktime(self.lastModified.timetuple())

class Suggestions(Base):
    __tablename__ = 'suggestions'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    album = Column(String)
    artist = Column(String)
    suggestor = Column(String)
    comments = Column(String)

class User(Base):
    __tablename__ = 'users'
    username = Column('uname', String, primary_key=True)
    password = Column('pword', String(64))

class SiteOptions(Base):
    __tablename__ = "site_options"
    id = Column(Integer, primary_key=True)
    show_title = Column(String)
    show_time = Column(String)
    show_end = Column(String)
    limit_requests = Column(String)
    offset = Column(Integer)

class Listeners(Base):
    __tablename__ = "listeners"
    id = Column(Integer, primary_key=True)
    current = Column(Integer)
    max = Column(Integer)
