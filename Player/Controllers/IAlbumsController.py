from abc import ABC, abstractmethod

from Models.Database.AlbumDb import AlbumDb


class IAlbumsController(ABC):

    @abstractmethod
    def createAlbum(self, name: str):
        raise NotImplementedError

    @abstractmethod
    def deleteAlbum(self, name: str):
        raise NotImplementedError

    @abstractmethod
    def addMusicToAlbum(self, name: str, musicPath: str):
        raise NotImplementedError

    @abstractmethod
    def removeMusicFromAlbum(self, name: str, musicPath: str):
        raise NotImplementedError

    @abstractmethod
    def exportAlbum(self, name: str):
        raise NotImplementedError

    @abstractmethod
    def importAlbum(self):
        raise NotImplementedError

    @abstractmethod
    def addAlbumToQueue(self, album: AlbumDb):
        raise NotImplementedError