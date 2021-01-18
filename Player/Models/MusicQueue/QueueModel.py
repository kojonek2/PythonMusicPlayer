import os
from typing import List

from Models.Data.Music import Music
from Models.Database.AlbumDb import AlbumDb

from win32com.shell import shell, shellcon

from Models.MusicQueue.AbstractMusicSelector import AbstractMusicSelector
from Models.MusicQueue.AlbumEntry import AlbumEntry


class QueueModel:

    def __init__(self, musicSelector: AbstractMusicSelector):
        self.queue = []
        self.selectedPosition = None
        self.musicSelector: AbstractMusicSelector = musicSelector

    def setMusicSelector(self, musicSelector: AbstractMusicSelector):
        self.musicSelector = musicSelector

    def selectNex(self):
        if self.musicSelector is None:
            return

        self.selectedPosition = self.musicSelector.nextSelection(self.queue, self.selectedPosition)
        if self.selectedPosition is None:
            return

        entry = self.queue[self.selectedPosition[0]]
        if isinstance(entry, AlbumEntry):
            music = entry.music[self.selectedPosition[1]]
        else:
            music = entry

        if self.__isMusicMissing(music):
            self.selectNex()  # try again because this track is missing on disc

    def getSelectedMusic(self):
        if self.selectedPosition is None:
            return None

        entry = self.queue[self.selectedPosition[0]]
        if isinstance(entry, AlbumEntry):
            music = entry.music[self.selectedPosition[1]]
        else:
            music = entry

        return music

    def addAlbumToQueue(self, album: AlbumDb):
        entry = AlbumEntry(album.name)

        for mDb in album.music:
            filename = os.path.basename(mDb.path)
            m = Music(filename, mDb.path)

            if not self.__isMusicMissing(m):
                entry.music.append(m)  # check if music is not missing

        if len(entry.music) <= 0:
            return

        self.queue.append(entry)

        if self.selectedPosition is None:  # if there was no music select it
            self.selectNex()

    def addMusicToQueue(self, music: Music):
        if not self.__isMusicMissing(music):
            self.queue.append(music)  # check if music is not missing

            if self.selectedPosition is None:  # if there was no music select it
                self.selectNex()

    def clear(self):
        self.queue = []
        self.selectedPosition = None

    def __isMusicMissing(self, music: Music) -> bool:
        musicFolder = shell.SHGetFolderPath(0, shellcon.CSIDL_MYMUSIC, None, 0)
        path = os.path.join(musicFolder, music.path)
        return not os.path.isfile(path)
