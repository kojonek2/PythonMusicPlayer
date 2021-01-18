import os
from typing import Callable

from Controllers.IAlbumsController import IAlbumsController
from Controllers.IMenuController import IMenuController
from Controllers.IMusicController import IMusicController
from Controllers.IOnlineRadiosController import IOnlineRadiosController
from Controllers.IPlayerController import IPlayerController
from Models.ClassificationModel import ClassificationModel
from Models.Database.AlbumDb import AlbumDb
from Models.Database.SkipDb import SkipDb
from Models.IRunnerOnMainThread import IRunnerOnMainThread
from Models.MainModel import MainModel
from Models.Data.Music import Music
from Models.Player import Player
from Models.RadioStation import RadioStation
from Models.SerializationModel import SerializationModel
from Views.IMainWindow import IMainWindow
from Views.MainWindow import MainWindow

from tkinter import filedialog
from tkinter import messagebox

ALBUM_EXTENSION = '.alb'


class MainController(IMenuController, IOnlineRadiosController, IPlayerController, IMusicController, IAlbumsController, IRunnerOnMainThread):

    def __init__(self):
        self.player = Player(self)
        self.mainModel = MainModel(self.player)
        self.classificationModel = ClassificationModel()
        self.serializationModel = SerializationModel()

        self.mainWindow: IMainWindow = MainWindow()

        self.mainWindow.setMenuController(self)
        self.mainWindow.setOnlineRadiosController(self)
        self.mainWindow.setPlayerController(self)
        self.mainWindow.setMusicController(self)
        self.mainWindow.setAlbumsController(self)

        self.mainModel.addDisplayViewUpdatedListener(self.mainWindow)
        self.player.addPlayerStateUpdatedListener(self.mainWindow)

        self.mainWindow.mainLoop()

    def onRadiosOnlineClicked(self):
        self.mainModel.displayRadioSelection()

    def onRadioSelected(self, radio: RadioStation):
        self.mainModel.playRadio(radio)

    def onVolumeSelected(self, volume: int):
        self.player.setVolume(volume)

    def onPredictGenreClicked(self):
        messagebox.showinfo("Information", "Please select music file")
        file = filedialog.askopenfilename()
        if file is None or file == '':
            return

        try:
            genre = self.classificationModel.predictGenre(file)
            messagebox.showinfo("Information", f"Genre: {genre}")
        except:
            messagebox.showerror("Error", "Could not predict genre!")

    def onMusicMenuButtonClicked(self):
        self.mainModel.displayMusicSelection()

    def onAlbumsMenuButtonClicked(self):
        self.mainModel.displayAlbumsSelection()

    def onQueueMenuButtonClicked(self):
        self.mainModel.displayQueue()

    def onSkipDeleteClicked(self, skip: SkipDb):
        self.mainModel.mainModelDeleteSkip(skip)

    def onSkipAddClicked(self, musicPath: str, start: int, end: int):
        self.mainModel.mainModelAddSkip(musicPath, start, end)

    def onMusicDoubleClicked(self, music: Music):
        self.mainModel.addMusicToQueue(music)

    def seekTo(self, percentage: float):
        self.player.seekTo(percentage)

    def onPlayPauseClicked(self):
        self.player.playPause()

    def createAlbum(self, name: str):
        if name is None or name == '':
            messagebox.showwarning('Error', 'Insert album name firstly!')
            return

        success = self.mainModel.createAlbum(name)
        if not success:
            messagebox.showwarning('Error', 'Album with that name already exists!')
            return

    def deleteAlbum(self, name: str):
        self.mainModel.deleteAlbum(name)

    def addMusicToAlbum(self, name: str, musicPath: str):
        error = self.mainModel.addMusicToAlbum(name, musicPath)

        if error is not None:
            messagebox.showwarning('Error', error)
            return

    def removeMusicFromAlbum(self, name: str, musicPath: str):
        error = self.mainModel.removeMusicFromAlbum(name, musicPath)

        if error is not None:
            messagebox.showwarning('Error', error)
            return

    def exportAlbum(self, name: str):
        filename = filedialog.asksaveasfilename(defaultextension='alb', filetypes=[('Album file', ALBUM_EXTENSION)])
        _, extension = os.path.splitext(filename)

        if extension != ALBUM_EXTENSION:
            messagebox.showwarning('Warning', f'Please select file with extension {ALBUM_EXTENSION}')
            return

        self.serializationModel.exportAlbum(name, filename)

    def importAlbum(self):
        filename = filedialog.askopenfilename(defaultextension='alb', filetypes=[('Album file', ALBUM_EXTENSION)])
        _, extension = os.path.splitext(filename)

        if extension != ALBUM_EXTENSION:
            messagebox.showwarning('Warning', f'Please select file with extension {ALBUM_EXTENSION}')
            return

        success = self.serializationModel.importAlbum(filename)
        if not success:
            messagebox.showwarning('Warning', f'Import failed! Possible file corruption!')
            return

        self.mainModel.albumImported()

    def runOnMainThread(self, callable: Callable):
        self.mainWindow.runOnEventLoop(callable)

    def addAlbumToQueue(self, album: AlbumDb):
        self.mainModel.addAlbumToQueue(album)

    def nextTrackClicked(self):
        self.mainModel.nextTrack()

    def changeMusicSelectionModeClicked(self):
        self.mainModel.changeMusicSelectionMode()
