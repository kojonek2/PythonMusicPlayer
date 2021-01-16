from sqlalchemy import Column, Integer, ForeignKey

from Models.Database.Database import Base


class SkipDb(Base):
    __tablename__ = 'skip'

    id = Column(Integer, primary_key=True)
    start = Column(Integer)
    end = Column(Integer)

    musicId = Column(Integer, ForeignKey('music.id'))
