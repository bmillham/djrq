from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Artist(Base):
    __tablename__ = 'artist'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    prefix = Column(String)

    @property
    def fullname(self):
        if self.prefix is None:
            return self.name
        else:
            return self.prefix + " " + self.name
