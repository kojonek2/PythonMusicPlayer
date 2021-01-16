from abc import ABC, abstractmethod

from Models.Database.SkipDb import SkipDb
from Models.Data.Music import Music


class IMusicController(ABC):

    @abstractmethod
    def onMusicDoubleClicked(self, music: Music):
        raise NotImplementedError

    @abstractmethod
    def onSkipDeleteClicked(self, skip: SkipDb):
        raise NotImplementedError

    @abstractmethod
    def onSkipAddClicked(self, musicPath: str, start: int, end: int):
        raise NotImplementedError
