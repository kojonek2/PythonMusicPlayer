from typing import List, Union, Tuple

from Models.Database.AlbumDb import AlbumDb
from Models.DisplayedView import DisplayedView
from Models.Data.Music import Music
from Models.RadioStation import RadioStation


class DisplayViewStatus:

    def __init__(self):
        self.currentDisplayedView = DisplayedView.WELCOME_SCREEN  # copied due to warning
        self.radioStations: List[RadioStation] = None
        self.music: List[Music] = None
        self.albums: List[AlbumDb] = None
        self.queue: List[Union[Music, AlbumDb]] = None
        self.selectionInQueue: Tuple[int, int] = None

    def clear(self):
        self.currentDisplayedView = DisplayedView.WELCOME_SCREEN
        self.radioStations: List[RadioStation] = None
        self.music: List[Music] = None
        self.albums: List[AlbumDb] = None
        self.queue: List[Union[Music, AlbumDb]] = None
        self.selectionInQueue: Tuple[int, int] = None
