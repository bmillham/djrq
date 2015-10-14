from . import *

class RequestList(Base):
    __tablename__= 'requestlist'

    id = Column(Integer, primary_key=True)
    song_id = Column('songID', Integer, ForeignKey('cc_files.id'))
    t_stamp = Column(DateTime, server_default=func.now())
    host = Column(String)
    msg = Column(String)
    name = Column(String)
    code = Column(Integer)
    eta = Column('ETA', DateTime)
    status = Column(Enum('played', 'ignored', 'pending', 'new', name='request_enum'))