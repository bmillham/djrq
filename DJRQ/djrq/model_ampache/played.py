from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TIMESTAMP

Base = declarative_base()

class Played(Base):
    __tablename__ = 'played'
    played_id = Column(Integer, primary_key=True)
    track_id = Column(Integer, ForeignKey('song.id'))
    date_played = Column(TIMESTAMP)
    played_by = Column(String)
    played_by_me = Column(Integer)