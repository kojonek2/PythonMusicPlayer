from tkinter import Frame, Button, SUNKEN, RAISED, SOLID, GROOVE

from Controllers.IMenuController import IMenuController

WIDTH = 200
ONLINE_RADIOS_TEXT = 'Online radios'
PREDICT_GENRE_TEXT = 'Predict genre'
MUSIC_TEXT = 'Music'
ALBUMS_TEXT = 'Albums'
QUEUE_TEXT = 'Queue'
BUTTON_HEIGHT = 2

class MenuPanel(Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.__initView()

    def __initView(self):
        self.configure(width=WIDTH)
        self.configure(borderwidth=3, relief=GROOVE)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        self.onlineRadiosButton = Button(self, text=ONLINE_RADIOS_TEXT, height=BUTTON_HEIGHT)
        self.onlineRadiosButton.grid(row=0, column=0, sticky='WE')
        self.onlineRadiosButton.configure(relief=RAISED)

        self.predictGenreButton = Button(self, text=PREDICT_GENRE_TEXT, height=BUTTON_HEIGHT)
        self.predictGenreButton.grid(row=1, column=0, sticky='WE')
        self.predictGenreButton.configure(relief=RAISED)

        self.musicButton = Button(self, text=MUSIC_TEXT, height=BUTTON_HEIGHT)
        self.musicButton.grid(row=2, column=0, sticky='WE')
        self.musicButton.configure(relief=RAISED)

        self.albumsButton = Button(self, text=ALBUMS_TEXT, height=BUTTON_HEIGHT)
        self.albumsButton.grid(row=3, column=0, sticky='WE')
        self.albumsButton.configure(relief=RAISED)

        self.queueButton = Button(self, text=QUEUE_TEXT, height=BUTTON_HEIGHT)
        self.queueButton.grid(row=4, column=0, sticky='WE')
        self.queueButton.configure(relief=RAISED)

    def setMenuController(self, menuController: IMenuController):
        self.onlineRadiosButton.configure(command=menuController.onRadiosOnlineClicked)
        self.predictGenreButton.configure(command=menuController.onPredictGenreClicked)
        self.musicButton.configure(command=menuController.onMusicMenuButtonClicked)
        self.albumsButton.configure(command=menuController.onAlbumsMenuButtonClicked)
        self.queueButton.configure(command=menuController.onQueueMenuButtonClicked)

