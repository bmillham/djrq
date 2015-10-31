from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RequestList(Base):
    __tablename__= 'requestlist'
    id = Column(Integer, primary_key=True)
    song_id = Column('songID', Integer)
    t_stamp = Column(DateTime)
    host = Column(String)
    msg = Column(String)
    name = Column(String)
    code = Column(Integer)
    eta = Column('ETA', DateTime)
    status = Column(Enum('played', 'ignored', 'pending', 'new'))