from typing import List

import vlc

from Models.Listeners.IPlayerStateListener import IPlayerStateListener
from Models.Listeners.IPlayerStateObservable import IPlayerStateObservable
from Models.PlayerState import PlayerState, PlaybackState, TrackType


class Player(IPlayerStateObservable):

    def __init__(self):
        self.playerStateListeners: List[IPlayerStateListener] = []
        self.playerState = PlayerState()

        self.vlcInstance: vlc.Instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        self.player: vlc.MediaPlayer = self.vlcInstance.media_player_new()

    def setOnlineStream(self, streamUrl):
        media = self.vlcInstance.media_new(streamUrl)
        self.player.set_media(media)
        self.playerState.trackType = TrackType.RADIO
        self.__notifyPlayerStateUpdate()

    def setTrackName(self, name: str):
        self.playerState.trackName = name
        self.__notifyPlayerStateUpdate()

    def play(self):
        self.player.play()
        self.playerState.playbackState = PlaybackState.PLAYING
        self.__notifyPlayerStateUpdate()

    def setVolume(self, volume):
        self.player.audio_set_volume(volume)

    # region IPlayerStateObservable
    def __notifyPlayerStateUpdate(self):
        for listener in self.playerStateListeners:
            listener.onPlayerStateUpdated(self.playerState)

    def addPlayerStateUpdatedListener(self, listener: IPlayerStateListener):
        if listener not in self.playerStateListeners:
            self.playerStateListeners.append(listener)
            listener.onPlayerStateUpdated(self.playerState)

    def removePlayerStateUpdatedListener(self, listener: IPlayerStateListener):
        if listener in self.playerStateListeners:
            self.playerStateListeners.remove(listener)
    # endregion

