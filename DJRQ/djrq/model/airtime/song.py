from . import *
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property

class Song(Base):
    __tablename__ = "cc_files"
    id = Column(Integer, primary_key=True)
    title = Column("track_title", String(512))
    artist_fullname = Column("artist_name", String(512))
    album_fullname = Column("album_title", String(512))
    catalog = Column("directory", Integer, ForeignKey('cc_music_dirs.id'))
    #catalog = relationship("Catalog", backref="songs")
    filepath = Column(Text)
    year = Column(String(16))
    bit_rate = Column(Integer)
    sample_rate = Column(Integer)
    _time = Column('length', Interval)
    track = Column('track_number', Integer)
    addition_time = Column('utime', DateTime)
    played = relationship("Played", backref="song")
    #requests = relationship("RequestList", backref='song', order_by='RequestList.t_stamp.desc()')
    new_requests = relationship("RequestList", 
        primaryjoin="and_(RequestList.song_id==Song.id, or_(RequestList.status == 'new', RequestList.status=='pending'))")
    played_requests = relationship("RequestList",
                       primaryjoin="and_(RequestList.song_id==Song.id, RequestList.status == 'played')",
                       order_by="RequestList.t_stamp.desc()")
    last_request = relationship("RequestList",\
                                primaryjoin="RequestList.song_id==Song.id",\
                                uselist=False, order_by='RequestList.t_stamp.desc()')
    mistags = relationship("Mistags", backref='song')

    artist_prefix = column_property(func.get_prefix(artist_fullname, prefixes))
    artist_name = column_property(func.no_prefix(artist_fullname, prefixes))
    album_prefix = column_property(func.get_prefix(album_fullname, prefixes))
    album_name = column_property(func.no_prefix(album_fullname, prefixes))

    @hybrid_property
    def file(self):
        return self.catalog.directory + self.filepath

    @hybrid_property
    def size(self):
        return round((float(self.bit_rate) * self.time) / 8.0) # Estimate the filesize

    @size.expression
    def size(self):
        return func.round((self.bit_rate * self.time) / 8.0)

    @hybrid_property
    def time(self):
        try:
            return self._time.total_seconds()
        except:
            return 0

    @time.expression
    def time(self):
        return func.extract("EPOCH", self._time)
