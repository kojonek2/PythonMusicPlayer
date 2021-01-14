from abc import ABC, abstractmethod

from Models.RadioStation import RadioStation


class IPlayerController(ABC):

    @abstractmethod
    def onVolumeSelected(self, volume: int):
        raise NotImplementedError

    @abstractmethod
    def seekTo(self, percentage: float):
        raise NotImplementedError

    @abstractmethod
    def onPlayPauseClicked(self):
        raise NotImplementedError
