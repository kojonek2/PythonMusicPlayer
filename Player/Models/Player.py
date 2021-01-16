from typing import List

import vlc
import os

from Models.Listeners.IPlayerStateListener import IPlayerStateListener
from Models.Listeners.IPlayerStateObservable import IPlayerStateObservable
from Models.PlayerState import PlayerState, PlaybackState, TrackType

from win32com.shell import shell, shellcon

from Models.Services.SkipService import SkipService


class Player(IPlayerStateObservable):

    def __init__(self):
        self.playerStateListeners: List[IPlayerStateListener] = []
        self.playerState = PlayerState()

        self.vlcInstance: vlc.Instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        self.player: vlc.MediaPlayer = self.vlcInstance.media_player_new()

        self.skips = None

        events: vlc.EventManager = self.player.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerLengthChanged, self.lengthChanged)
        events.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.positionChanged)
        self.volume = 50

    def lengthChanged(self, event):
        self.playerState.trackLength = int(event.u.new_length / 1000)
        self.playerState.trackPosition = event.u.new_position
        self.__notifyPlayerStateUpdate()

    def positionChanged(self, event):
        self.player.audio_set_volume(self.volume)
        self.playerState.trackPosition = event.u.new_position
        self.__notifyPlayerStateUpdate()

        self.__checkSkips(int(self.player.get_length() * event.u.new_position / 1000))

    def __checkSkips(self, positionInSeconds):
        if self.skips is not None:
            skips = self.skips.copy()
            skips = filter(lambda s: positionInSeconds < s.end, skips)
            skips = sorted(skips, key=lambda s: s.start)

            if len(skips) <= 0:
                return

            s = skips[0]
            if positionInSeconds >= s.start:
                trackLengthInMs = self.player.get_length()
                self.player.set_position(s.end * 1000 / trackLengthInMs)

    def setOnlineStream(self, streamUrl):
        self.player.stop()
        self.skips = None

        media = self.vlcInstance.media_new(streamUrl)
        self.player.set_media(media)
        self.playerState.trackType = TrackType.RADIO
        self.__notifyPlayerStateUpdate()

    def setMusic(self, musicPath):
        self.player.stop()

        skipsService = SkipService()
        self.skips = skipsService.getSkipsForMusic(musicPath)

        musicFolder = shell.SHGetFolderPath(0, shellcon.CSIDL_MYMUSIC, None, 0)
        path = os.path.join(musicFolder, musicPath)
        media = self.vlcInstance.media_new(path)
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
        self.volume = volume
        self.player.audio_set_volume(volume)

    def seekTo(self, percentage):
        if self.playerState.trackType != TrackType.MUSIC:
            return

        self.player.set_position(percentage)

    def playPause(self):
        if self.playerState.playbackState == PlaybackState.PLAYING:
            self.player.pause()
            self.playerState.playbackState = PlaybackState.PAUSED
        elif self.playerState.playbackState == PlaybackState.PAUSED:
            self.player.play()
            self.playerState.playbackState = PlaybackState.PLAYING
        self.__notifyPlayerStateUpdate()

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

