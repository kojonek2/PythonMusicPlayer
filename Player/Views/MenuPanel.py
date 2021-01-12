from tkinter import Frame, Button, SUNKEN, RAISED, SOLID, GROOVE

from Controllers.IMenuController import IMenuController

WIDTH = 200
ONLINE_RADIOS_TEXT = 'Online radios'
PREDICT_GENRE_TEXT = 'Predict genre'
BUTTON_HEIGHT = 2

class MenuPanel(Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.menuController: IMenuController = None

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

    def setMenuController(self, menuController: IMenuController):
        self.menuController = menuController
        self.onlineRadiosButton.configure(command=menuController.onRadiosOnlineClicked)
        self.predictGenreButton.configure(command=menuController.onPredictGenreClicked)

