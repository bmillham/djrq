from . import *

class Song(Base):
    __tablename__ = 'song'

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
    played = relationship("Played", backref=backref('song'), order_by="Played.date_played.desc()")
    requests = relationship("RequestList", backref=backref('song'), order_by="RequestList.t_stamp.desc()")
    played_requests = relationship("RequestList",
                                   primaryjoin="and_(RequestList.song_id==Song.id, RequestList.status == 'played')",
                                   order_by="RequestList.t_stamp.desc()")
    new_requests = relationship("RequestList", 
                                primaryjoin="and_(RequestList.song_id==Song.id, or_(RequestList.status == 'new', RequestList.status=='pending'))")
    mistags = relationship("Mistags", backref=backref('song'))

