from typing import List

from Models.Database.SkipDb import SkipDb
from Models.DisplayViewStatus import DisplayViewStatus
from Models.DisplayedView import DisplayedView
from Models.Listeners.IDisplayViewUpdatedListener import IDisplayViewUpdatedListener
from Models.Listeners.IDisplayViewUpdatedObservable import IDisplayViewUpdatedObservable
from Models.Data.Music import Music
from Models.RadioStation import RadioStation

from win32com.shell import shell, shellcon

import json
import os

from Models.Services.SkipService import SkipService

RADIO_STATIONS_FILE = 'radioStations.json'
NAME_KEY = 'name'
STREAM_URL_KEY = 'streamURL'
PATH_TO_IMAGE_KEY = 'imagePath'
MUSIC_FILE_EXTENSIONS = ['.mp3', '.wav']

class MainModel(IDisplayViewUpdatedObservable):

    def __init__(self):
        self.displayViewUpdatedListeners: List[IDisplayViewUpdatedListener] = []
        self.currentDisplayStatus = DisplayViewStatus()

    def displayRadioSelection(self):
        self.currentDisplayStatus.clear()
        self.currentDisplayStatus.currentDisplayedView = DisplayedView.ONLINE_RADIOS
        self.currentDisplayStatus.radioStations = self.readRadioStations()
        self.__notifyDisplayViewUpdated()

    def readRadioStations(self) -> List[RadioStation]:
        # return [RadioStation('Radio Zet', 'https://n-4-14.dcs.redcdn.pl/sc/o2/Eurozet/live/audio.livx', 'Images/radio_zet.jpg'),
        #         RadioStation('RMF FM', 'https://rs9-krk2-cyfronet.rmfstream.pl/RMFFM48', 'Images/rmf.png')]
        if not os.path.isfile(RADIO_STATIONS_FILE):
            return None

        try:
            with open(RADIO_STATIONS_FILE) as file:
                data = json.load(file)

            result = []

            for jsonRadio in data:
                if NAME_KEY not in jsonRadio:
                    continue

                if STREAM_URL_KEY not in jsonRadio:
                    continue

                if PATH_TO_IMAGE_KEY not in jsonRadio:
                    continue

                result.append(RadioStation(jsonRadio[NAME_KEY], jsonRadio[STREAM_URL_KEY], jsonRadio[PATH_TO_IMAGE_KEY]))

            return result
        except:
            return None

    def displayMusicSelection(self):
        self.currentDisplayStatus.clear()
        self.currentDisplayStatus.currentDisplayedView = DisplayedView.MUSIC_SCREEN
        self.currentDisplayStatus.music = self.musicFiles()
        self.__notifyDisplayViewUpdated()

    def musicFiles(self) -> List[Music]:
        musicFiles = []


        musicFolder = shell.SHGetFolderPath(0, shellcon.CSIDL_MYMUSIC, None, 0)
        for root, dirs, files in os.walk(musicFolder):
            for file in files:
                filename, extension = os.path.splitext(file)
                if extension in MUSIC_FILE_EXTENSIONS:
                    folder = os.path.relpath(root, musicFolder)
                    musicFiles.append(Music(file, os.path.join(folder, file)))

        skipService = SkipService()
        for music in musicFiles:
            music.skips = skipService.getSkipsForMusic(music.path)

        return musicFiles

    def mainModelDeleteSkip(self, skip: SkipDb):
        skipService = SkipService()
        skipService.deleteSkipsForMusic(skip.id)
        self.currentDisplayStatus.music = self.musicFiles()  # refresh skips
        self.__notifyDisplayViewUpdated()

    def mainModelAddSkip(self,  musicPath: str, start: int, end: int):
        skipService = SkipService()
        skipService.addSkipForMusic(musicPath, start, end)
        self.currentDisplayStatus.music = self.musicFiles()  # refresh skips
        self.__notifyDisplayViewUpdated()


    # region IDisplayViewUpdatedObservable
    def __notifyDisplayViewUpdated(self):
        for listener in self.displayViewUpdatedListeners:
            listener.onDisplayViewUpdated(self.currentDisplayStatus)

    def addDisplayViewUpdatedListener(self, listener: IDisplayViewUpdatedListener):
        if listener not in self.displayViewUpdatedListeners:
            self.displayViewUpdatedListeners.append(listener)
            listener.onDisplayViewUpdated(self.currentDisplayStatus)

    def removeDisplayViewUpdatedListener(self, listener: IDisplayViewUpdatedListener):
        if listener in self.displayViewUpdatedListeners:
            self.displayViewUpdatedListeners.remove(listener)
    # endregion
