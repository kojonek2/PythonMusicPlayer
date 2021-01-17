from sqlalchemy.orm import joinedload

from Models.Database.AlbumDb import AlbumDb
from Models.Database.Database import Database
from Models.Database.MusicDb import MusicDb


class AlbumService:

    def __init__(self):
        self.__db = Database()

    def getAlbums(self):
        session = self.__db.crateSession()

        albums = session.query(AlbumDb).options(joinedload(AlbumDb.music)).all()

        albums = list(albums)
        session.close()

        return albums

    def getAlbum(self, name):
        session = self.__db.crateSession()

        album = session.query(AlbumDb).options(joinedload(AlbumDb.music)).filter(AlbumDb.name == name).first()

        session.close()

        return album

    def createAlbum(self, name):
        session = self.__db.crateSession()

        duplicate = session.query(AlbumDb).filter(AlbumDb.name == name).first()
        if duplicate is not None:
            raise ValueError('Duplicate name')

        album = AlbumDb(name=name)
        session.add(album)

        session.commit()
        session.close()

    def addMusic(self, name, path):
        session = self.__db.crateSession()

        music = session.query(MusicDb).filter(MusicDb.path == path).first()
        if music is None:
            music = MusicDb(path=path)
            session.add(music)

        album = session.query(AlbumDb).filter(AlbumDb.name == name).first()
        if album is None:
            raise ValueError('Non existent album!')

        if music in album.music:
            raise ValueError('Music is already in album!')

        album.music.append(music)

        session.commit()
        session.close()

    def removeMusic(self, name, path):
        session = self.__db.crateSession()

        album = session.query(AlbumDb).filter(AlbumDb.name == name).first()
        if album is None:
            raise ValueError('Non existent album!')

        music = session.query(MusicDb).filter(MusicDb.path == path).first()
        if music is None:
            raise ValueError('Music is not in the database!')

        if music not in album.music:
            raise ValueError('Music is not in the album!')

        album.music.remove(music)

        session.commit()
        session.close()

    def deleteAlbum(self, name):
        session = self.__db.crateSession()

        album = session.query(AlbumDb).options(joinedload(AlbumDb.music)).filter(AlbumDb.name == name).first()
        if album is None:
            return

        album.music.clear()
        session.delete(album)

        session.commit()
        session.close()
