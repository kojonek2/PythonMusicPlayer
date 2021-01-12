from abc import ABC, abstractmethod

from Models.Listeners.IPlayerStateListener import IPlayerStateListener


class IPlayerStateObservable(ABC):

    @abstractmethod
    def addPlayerStateUpdatedListener(self, listener: IPlayerStateListener):
        raise NotImplementedError

    @abstractmethod
    def removePlayerStateUpdatedListener(self, listener: IPlayerStateListener):
        raise NotImplementedError
