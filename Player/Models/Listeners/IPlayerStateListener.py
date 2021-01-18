from abc import ABC, abstractmethod

from Models.PlayerState import PlayerState


class IPlayerStateListener(ABC):

    @abstractmethod
    def onPlayerStateUpdated(self, state: PlayerState):
        raise NotImplementedError

    @abstractmethod
    def onPlayerEndReached(self):
        raise NotImplementedError
