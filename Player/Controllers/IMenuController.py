from abc import ABC, abstractmethod


class IMenuController(ABC):

    @abstractmethod
    def onRadiosOnlineClicked(self):
        raise NotImplementedError

    @abstractmethod
    def onPredictGenreClicked(self):
        raise NotImplementedError

    @abstractmethod
    def onMusicMenuButtonClicked(self):
        raise NotImplementedError

    @abstractmethod
    def onAlbumsMenuButtonClicked(self):
        raise NotImplementedError

    @abstractmethod
    def onQueueMenuButtonClicked(self):
        raise NotImplementedError
