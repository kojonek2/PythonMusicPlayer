from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from Models.Database.Database import Base


class PlayEntryDb(Base):
    __tablename__ = 'playEntry'

    id = Column(Integer, primary_key=True)
    dateTime = Column(DateTime)

    musicId = Column(Integer, ForeignKey('music.id'))
    music = relationship('MusicDb')
