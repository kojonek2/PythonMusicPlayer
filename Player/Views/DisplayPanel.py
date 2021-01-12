from tkinter import Frame, Label, CENTER

from Controllers.IOnlineRadiosController import IOnlineRadiosController
from Models.DisplayViewStatus import DisplayViewStatus
from Models.DisplayedView import DisplayedView
from Models.Listeners.IDisplayViewUpdatedListener import IDisplayViewUpdatedListener
from Views.OnlineRadiosPanel import OnlineRadiosPanel

WELCOME_TEXT = 'Welcome to Song Player application!'

class DisplayPanel(Frame, IDisplayViewUpdatedListener):

    def __init__(self, parent):
        super().__init__(parent)

        self.welcomePanel: Frame = None
        self.radioPanel: OnlineRadiosPanel = None

        self.__viewInit()

    def setOnlineRadiosController(self, radioController: IOnlineRadiosController):
        self.radioPanel = OnlineRadiosPanel(self, radioController)

    def __viewInit(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.welcomePanel = Frame(self)
        welcomeText = Label(self.welcomePanel, text=WELCOME_TEXT, font=("Arial", 25))
        welcomeText.place(relx=0.5, rely=0.5, anchor=CENTER)

    def onDisplayViewUpdated(self, status: DisplayViewStatus):
        for widget in self.grid_slaves():
            widget.grid_forget()

        if status.currentDisplayedView is DisplayedView.WELCOME_SCREEN:
            self.welcomePanel.grid(row=0, column=0, sticky='NSWE')
        elif status.currentDisplayedView is DisplayedView.ONLINE_RADIOS and self.radioPanel is not None:
            self.radioPanel.grid(row=0, column=0, sticky='NSWE')
            self.radioPanel.displayRadios(status.radioStations)
