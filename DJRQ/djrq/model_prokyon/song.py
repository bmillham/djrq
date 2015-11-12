from . import *
from datetime import datetime

class Name(object):
    def __init__(self, type, fullname, name, prefix):
        self._type = type
        self._fullname = fullname
        self._prefix = prefix
        self._name = name
        #print "In name: fullname: ", fullname
        #for p in prefixes:
        #    if fullname.lower().startswith(p.lower() + " "):
        #        self._prefix = p
        #        self._name = fullname.split(' ', 1)[1]
        #        break
        #if not self._prefix:
        #    self._name = fullname

    def __unicode__(self):
        from urllib import quote_plus, quote
        return u'<a href="/{}/name/{}">{}</a>'.format(self._type, quote(self._fullname.encode('utf8')), self._fullname)

    @property
    def name(self):
        return self._name
    
    @property
    def prefix(self):
        return self._prefix

    @property
    def fullname(self):
        return self._fullname

    @property
    def new_link(self):
        return u'<a href="/{}/new/name/{}">{}</a>'.format(self._type, quote(self._fullname.encode('utf8')), self._fullname)

    @property
    def songs(self):
        return session.query(Song).filter(eval("Song.{}_fullname".format(self._type))==self._fullname)

class Song(Base):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True)
    title = Column("title", String(255))
    artist_fullname = Column("artist", String(255))
    album_fullname = Column("album", String(255))
    path = Column(String(255))
    filename = Column(String(255))
    year = Column(String(255))
    bit_rate = Column("bitrate", Integer)
    sample_rate = Column("samplerate", Integer)
    time = Column('length', Integer)
    track = Column('tracknumber', Integer)
    _addition_time = Column('lastModified', DateTime)
    size = Column(Integer)

    played = relationship("Played", backref="song")
    requests = relationship("RequestList", backref='song', order_by='RequestList.t_stamp.desc()')
    new_requests = relationship("RequestList", 
        primaryjoin="and_(RequestList.song_id==Song.id, or_(RequestList.status == 'new', RequestList.status=='pending'))")
    played_requests = relationship("RequestList",
                       primaryjoin="and_(RequestList.song_id==Song.id, RequestList.status == 'played')",
                       order_by="RequestList.t_stamp.desc()")
    last_request = relationship("RequestList",\
                                primaryjoin="RequestList.song_id==Song.id",\
                                uselist=False, order_by='RequestList.t_stamp.desc()')
    mistags = relationship("Mistags", backref='song')

    album_prefix = column_property(func.if_(album_fullname.like('the %'), func.substring_index(album_fullname, ' ', 1), ''))
    album_name = column_property(func.if_(album_fullname.like('the %'), func.substring(album_fullname, func.locate(' ', album_fullname)+1), album_fullname))
    artist_prefix = column_property(func.if_(artist_fullname.like('The %'), func.substring_index(artist_fullname, ' ', 1), ''))
    artist_name = column_property(func.if_(artist_fullname.like('The %'), func.substring(artist_fullname, func.locate(' ', artist_fullname)+1), artist_fullname))

    @hybrid_property
    def addition_time(self):
        return (self._addition_time - datetime(1970, 1, 1)).total_seconds()

    @addition_time.expression
    def addition_time(self):
        return func.unix_timestamp(self._addition_time)

    @hybrid_property
    def catalog(self):
        return '1'

    @catalog.expression
    def catalog(self):
        return '1'

    @hybrid_property
    def file(self):
        return self.path + self.filepath

    @hybrid_property
    def album_id(self):
        return self.album_fullname

    @hybrid_property
    def artist_id(self):
        return self.artist_fullname

    @hybrid_property
    def album(self):
        return Name('album', self.album_fullname, self.album_name, self.album_prefix)
    
    @hybrid_property
    def artist(self):
        print "Creating artist: %s, %s" % (self.artist_name, self.artist_prefix)
        return Name('artist', self.artist_fullname, self.artist_name, self.artist_prefix)

"""    @hybrid_property
    def artist_prefix(self):
        return Name('album', self.artist_fullname).prefix

    @hybrid_property
    def artist_name(self):
        return Name('album', self.artist_fullname).name

    @hybrid_property
    def album_prefix(self):
        return Name('album', self.album_fullname).prefix

    @hybrid_property
    def album_name(self):
        return Name('album', self.album_fullname).name"""



