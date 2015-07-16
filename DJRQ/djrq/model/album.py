from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Album(Base):
    __tablename__ = 'album'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    prefix = Column(String)
    year = Column(Integer)
    disk = Column(SmallInteger)

    @property
    def fullname(self):
        if self.prefix is None:
            return self.name
        else:
            return self.prefix + " " + self.name