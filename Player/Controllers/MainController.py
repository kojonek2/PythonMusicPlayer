from Controllers.IMenuController import IMenuController
from Controllers.IOnlineRadiosController import IOnlineRadiosController
from Controllers.IPlayerController import IPlayerController
from Models.ClassificationModel import ClassificationModel
from Models.MainModel import MainModel
from Models.Player import Player
from Models.RadioStation import RadioStation
from Views.IMainWindow import IMainWindow
from Views.MainWindow import MainWindow

from tkinter import filedialog
from tkinter import messagebox

class MainController(IMenuController, IOnlineRadiosController, IPlayerController):



    def __init__(self):
        self.player = Player()
        self.mainModel = MainModel()
        self.classificationModel = ClassificationModel()

        self.mainWindow: IMainWindow = MainWindow()

        self.mainWindow.setMenuController(self)
        self.mainWindow.setOnlineRadiosController(self)
        self.mainWindow.setPlayerController(self)

        self.mainModel.addDisplayViewUpdatedListener(self.mainWindow)
        self.player.addPlayerStateUpdatedListener(self.mainWindow)

        self.mainWindow.mainLoop()

    def onRadiosOnlineClicked(self):
        self.mainModel.displayRadioSelection()

    def onRadioSelected(self, radio: RadioStation):
        self.player.setOnlineStream(radio.streamURL)
        self.player.setTrackName(radio.name)
        self.player.play()

    def onVolumeSelected(self, volume: int):
        self.player.setVolume(volume)

    def onPredictGenreClicked(self):
        messagebox.showinfo("Information", "Please select music file")
        file = filedialog.askopenfilename()

        try:
            genre = self.classificationModel.predictGenre(file)
            messagebox.showinfo("Information", f"Genre: {genre}")
        except:
            messagebox.showerror("Error", "Could not predict genre!")