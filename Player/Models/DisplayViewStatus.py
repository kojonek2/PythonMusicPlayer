from typing import List

from Models.DisplayedView import DisplayedView
from Models.Music import Music
from Models.RadioStation import RadioStation


class DisplayViewStatus:

    def __init__(self):
        self.currentDisplayedView = DisplayedView.WELCOME_SCREEN  # copied due to warning
        self.radioStations: List[RadioStation] = None
        self.music: List[Music] = None

    def clear(self):
        self.currentDisplayedView = DisplayedView.WELCOME_SCREEN
        self.radioStations: List[RadioStation] = None
        self.music: List[Music] = None

