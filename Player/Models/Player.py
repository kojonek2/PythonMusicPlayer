from typing import List

import vlc
import os

from Models.Listeners.IPlayerStateListener import IPlayerStateListener
from Models.Listeners.IPlayerStateObservable import IPlayerStateObservable
from Models.PlayerState import PlayerState, PlaybackState, TrackType

from win32com.shell import shell, shellcon


class Player(IPlayerStateObservable):

    def __init__(self):
        self.playerStateListeners: List[IPlayerStateListener] = []
        self.playerState = PlayerState()

        self.vlcInstance: vlc.Instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        self.player: vlc.MediaPlayer = self.vlcInstance.media_player_new()
        events: vlc.EventManager = self.player.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerLengthChanged, self.lengthChanged)

    def lengthChanged(self, event):
        self.playerState.trackLength = int(event.u.new_length / 1000)
        self.playerState.trackPosition = int(event.u.new_position / 1000)
        self.__notifyPlayerStateUpdate()

    def setOnlineStream(self, streamUrl):
        media = self.vlcInstance.media_new(streamUrl)
        self.player.set_media(media)
        self.playerState.trackType = TrackType.RADIO
        self.__notifyPlayerStateUpdate()

    def setMusic(self, musicPath):
        musicFolder = shell.SHGetFolderPath(0, shellcon.CSIDL_MYMUSIC, None, 0)
        path = os.path.join(musicFolder, musicPath)
        media = self.vlcInstance.media_new(path)
        media.parse()
        self.player.set_media(media)

        self.playerState.trackType = TrackType.MUSIC
        self.__notifyPlayerStateUpdate()

    def setTrackName(self, name: str):
        self.playerState.trackName = name
        self.__notifyPlayerStateUpdate()

    def play(self):
        self.player.play()
        self.playerState.playbackState = PlaybackState.PLAYING
        self.playerState.trackLength = self.player.get_length()
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

