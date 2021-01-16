from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from Models.Database.Database import Base


class MusicDb(Base):
    __tablename__ = 'music'

    id = Column(Integer, primary_key=True)
    path = Column(String)
    skips = relationship('SkipDb')
