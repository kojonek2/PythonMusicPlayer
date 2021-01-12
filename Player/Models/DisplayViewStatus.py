from typing import List

from Models.DisplayedView import DisplayedView
from Models.RadioStation import RadioStation


class DisplayViewStatus:

    def __init__(self):
        self.currentDisplayedView = DisplayedView.WELCOME_SCREEN
        self.radioStations: List[RadioStation] = None

