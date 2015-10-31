from . import *
from sqlalchemy.ext.hybrid import hybrid_property

class Played(Base):
    __tablename__ = 'cc_playout_history'

    id = Column(Integer, primary_key=True)
    track_id = Column("file_id", Integer, ForeignKey('cc_files.id'))
    date_played = Column("starts", DateTime)
    instance_id = Column(Integer)
    show = relationship("PlayedShow", uselist=False, backref="plays")

    @hybrid_property
    def played_by(self):
        return self.show.value

class PlayedShow(Base):
    __tablename__ = "cc_playout_history_metadata"

    id = Column(Integer, primary_key=True)
    history_id = Column(Integer, ForeignKey('cc_playout_history.id'))
    key = Column(String(128))
    value = Column(String(128))
