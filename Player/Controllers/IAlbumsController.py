from abc import ABC, abstractmethod


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