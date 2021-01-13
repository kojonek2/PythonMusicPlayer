from tkinter import Button, Label, RIDGE, Frame, Scale, HORIZONTAL, DISABLED
from tkinter.ttk import Progressbar

from PIL.ImageTk import PhotoImage
from PIL import Image

from Controllers.IPlayerController import IPlayerController
from Models.Listeners.IPlayerStateListener import IPlayerStateListener
from Models.PlayerState import PlayerState, TrackType, PlaybackState

HEIGHT = 100
PLAY_ICON = 'Images/play_icon.png'
PROGREESBAR_MULTIPLAYER = 5


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

        self.trackProgressBar = Progressbar(self, orient=HORIZONTAL, length=300, mode='determinate')
        self.trackProgressBar.grid(row=0, column=3)

    def onPlayerStateUpdated(self, state: PlayerState):
        self.trackNameLabel.configure(text=state.trackName)

        if state.trackType is TrackType.MUSIC:
            self.trackProgressBar.configure(maximum=state.trackLength * PROGREESBAR_MULTIPLAYER, value=state.trackPosition * PROGREESBAR_MULTIPLAYER)
            if state.playbackState is PlaybackState.PLAYING:
                self.trackProgressBar.start(int(1000 / PROGREESBAR_MULTIPLAYER))
            else:
                self.trackProgressBar.stop()

        else:
            self.trackProgressBar.stop()
            self.trackProgressBar.configure(value=0)

    def setPlayerController(self, playerController: IPlayerController):
        self.volumeScale.configure(command=lambda v: playerController.onVolumeSelected(self.volumeScale.get()))
        playerController.onVolumeSelected(self.volumeScale.get())
