from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *

Base = declarative_base()
from . import Album

class Song(Base):
    __tablename__ = 'song'
    id = Column(Integer, primary_key=True)
    file = Column(String)
    catalog = Column(Integer)
    album_id  = Column("album", Integer, ForeignKey('album.id'))
    year = Column(Integer)
    artist_id = Column("artist", Integer, ForeignKey('artist.id'))
    title = Column(String)
    size = Column(Integer)
    time = Column(SmallInteger)
    track = Column(SmallInteger)
    played = Column(SmallInteger)
    addition_time = Column(Integer)
    album = relationship("Album", backref=backref('songs', order_by=track))
    artist = relationship("Artist", backref=backref('songs', order_by=id))
    played = relationship("Played", backref=backref('song'))
    requests = relationship("RequestList", backref=backref('song'))