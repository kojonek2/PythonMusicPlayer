from enum import Enum


class TrackType(Enum):
    NONE = 0
    RADIO = 1
    MUSIC = 2


class PlaybackState(Enum):
    NONE = 0
    PLAYING = 1
    PAUSED = 2


class PlayerState:

    def __init__(self):
        self.trackName = ''
        self.trackType = TrackType.NONE
        self.playbackState = PlaybackState.NONE