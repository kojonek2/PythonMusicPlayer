from abc import ABC, abstractmethod
from typing import Tuple, List, Union

from Models.Data.Music import Music
from Models.MusicQueue.AlbumEntry import AlbumEntry

Queue = List[Union[Music, AlbumEntry]]
Position = Tuple[int, int]


class AbstractMusicSelector(ABC):

    @abstractmethod
    def nextSelection(self, queue: Queue, selectedPosition: Position) -> Position:
        raise NotImplementedError()
