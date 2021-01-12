from tkinter import Button, Label, RIDGE, Frame, Scale, HORIZONTAL

from PIL.ImageTk import PhotoImage
from PIL import Image

from Controllers.IPlayerController import IPlayerController
from Models.Listeners.IPlayerStateListener import IPlayerStateListener
from Models.PlayerState import PlayerState

HEIGHT = 100
PLAY_ICON = 'Images/play_icon.png'


class PlayerControlPanel(Frame, IPlayerStateListener):

    def __init__(self, parent):
        super().__init__(parent)
        self.trackNameLabel: Label = None
        self.volumeScale: Scale = Scale

        self.__initView()

    def __initView(self):
        self.configure(borderwidth=3, relief=RIDGE)
        self.configure(height=HEIGHT)

        self.trackNameLabel = Label(self)
        self.trackNameLabel.grid(row=0, column=0)

        image = Image.open(PLAY_ICON)
        image = image.resize((64, 64), Image.ANTIALIAS)
        self.icon = PhotoImage(image=image)
        playButton = Button(self, image=self.icon)
        playButton.grid(row=0, column=1)

        self.volumeScale = Scale(self, from_=0, to=100, orient=HORIZONTAL)
        self.volumeScale.set(50)
        self.volumeScale.grid(row=0, column=2)

    def onPlayerStateUpdated(self, state: PlayerState):
        self.trackNameLabel.configure(text=state.trackName)

    def setPlayerController(self, playerController: IPlayerController):
        self.volumeScale.configure(command=lambda v: playerController.onVolumeSelected(self.volumeScale.get()))
        playerController.onVolumeSelected(self.volumeScale.get())
