from abc import ABC, abstractmethod

from Models.Music import Music


class IMusicController(ABC):

    @abstractmethod
    def onMusicDoubleClicked(self, music: Music):
        raise NotImplementedError