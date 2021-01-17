from sqlalchemy import Column, Integer, Table, ForeignKey, String
from sqlalchemy.orm import relationship

from Models.Database.Database import Base

association_table = Table('album_music', Base.metadata,
                          Column('albumId', Integer, ForeignKey('album.id')),
                          Column('musicId', Integer, ForeignKey('music.id')))


class AlbumDb(Base):
    __tablename__ = 'album'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    music = relationship('MusicDb', secondary=association_table)
