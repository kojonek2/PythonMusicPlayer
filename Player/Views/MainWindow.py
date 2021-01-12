import tkinter as tk

from Controllers.IMenuController import IMenuController
from Controllers.IOnlineRadiosController import IOnlineRadiosController
from Controllers.IPlayerController import IPlayerController
from Models.DisplayViewStatus import DisplayViewStatus
from Models.PlayerState import PlayerState
from Views.DisplayPanel import DisplayPanel
from Views.IMainWindow import IMainWindow
from Views.MenuPanel import MenuPanel
from Views.PlayerControlPanel import PlayerControlPanel

TITLE = 'Music player'
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 650


class MainWindow(IMainWindow):

    def __init__(self):
        self.root: tk.Tk = None

        self.__initView()

    def setMenuController(self, menuController: IMenuController):
        self.menuPanel.setMenuController(menuController)

    def setOnlineRadiosController(self, radioController: IOnlineRadiosController):
        self.displayPanel.setOnlineRadiosController(radioController)

    def setPlayerController(self, playerController: IPlayerController):
        self.playerControlPanel.setPlayerController(playerController)

    def __initView(self):
        self.root = tk.Tk()
        self.root.title(TITLE)
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.root.resizable(False, False)
        self.__centerWindow()

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        #############################################################################

        menuPlusDisplayFrame = tk.Frame(self.root)
        menuPlusDisplayFrame.grid(row=0, column=0, sticky='EWNS')
        menuPlusDisplayFrame.grid_columnconfigure(1, weight=1)
        menuPlusDisplayFrame.grid_rowconfigure(0, weight=1)

        self.playerControlPanel = PlayerControlPanel(self.root)
        self.playerControlPanel.grid(row=1, column=0, sticky='EW')

        ##############################################################################

        self.menuPanel = MenuPanel(menuPlusDisplayFrame)
        self.menuPanel.grid(row=0, column=0, sticky='NS')

        self.displayPanel = DisplayPanel(menuPlusDisplayFrame)
        self.displayPanel.grid(row=0, column=1, sticky='NSWE')

    def __centerWindow(self):
        positionRight = int((self.root.winfo_screenwidth() - WINDOW_WIDTH) / 2)
        positionDown = int((self.root.winfo_screenheight() - WINDOW_HEIGHT) / 2)

        self.root.geometry(f"+{positionRight}+{positionDown}")

    def mainLoop(self):
        self.root.mainloop()

    def onDisplayViewUpdated(self, status: DisplayViewStatus):
        self.displayPanel.onDisplayViewUpdated(status)

    def onPlayerStateUpdated(self, state: PlayerState):
        self.playerControlPanel.onPlayerStateUpdated(state)
