from tkinter import Button, Label, RIDGE, Frame, Scale, HORIZONTAL, DISABLED, NORMAL
from tkinter.ttk import Progressbar

from PIL.ImageTk import PhotoImage
from PIL import Image

from Controllers.IPlayerController import IPlayerController
from Models.Listeners.IPlayerStateListener import IPlayerStateListener
from Models.PlayerState import PlayerState, TrackType, PlaybackState

HEIGHT = 100
PLAY_ICON = 'Images/play_icon.png'
PAUSE_ICON = 'Images/pause_icon.png'
MUTE_ICON = 'Images/mute_icon.png'
UNMUTE_ICON = 'Images/unmute_icon.png'
MAXIMUM = 1000


class PlayerControlPanel(Frame, IPlayerStateListener):

    def __init__(self, parent):
        super().__init__(parent)
        self.trackNameLabel: Label = None
        self.volumeScale: Scale = Scale

        self.muted = False

        self.__initView()

    def __initView(self):
        self.configure(borderwidth=3, relief=RIDGE)
        self.configure(height=HEIGHT)

        image = Image.open(PLAY_ICON)
        image = image.resize((32, 32), Image.ANTIALIAS)
        self.play_icon = PhotoImage(image=image)

        image = Image.open(PAUSE_ICON)
        image = image.resize((32, 32), Image.ANTIALIAS)
        self.pause_icon = PhotoImage(image=image)

        self.playPauseButton = Button(self, image=self.play_icon)
        self.playPauseButton.grid(row=0, column=0)

        image = Image.open(MUTE_ICON)
        image = image.resize((32, 32), Image.ANTIALIAS)
        self.mute_icon = PhotoImage(image=image)

        image = Image.open(UNMUTE_ICON)
        image = image.resize((32, 32), Image.ANTIALIAS)
        self.unmute_icon = PhotoImage(image=image)

        self.muteButton = Button(self, image=self.mute_icon, command=self.__muteButtonPressed)
        self.muteButton.grid(row=0, column=1)

        self.volumeScale = Scale(self, from_=0, to=100, orient=HORIZONTAL)
        self.volumeScale.set(50)
        self.volumeScale.grid(row=0, column=2)

        self.trackProgressBar = Progressbar(self, orient=HORIZONTAL, length=300, mode='determinate', maximum=MAXIMUM)
        self.trackProgressBar.grid(row=0, column=3)

        self.timeLabel = Label(self, text='--:--/--:--')
        self.timeLabel.grid(row=0, column=4)

        self.trackNameLabel = Label(self)
        self.trackNameLabel.grid(row=0, column=5)

    def onPlayerStateUpdated(self, state: PlayerState):
        self.trackNameLabel.configure(text=state.trackName)

        if state.trackType is TrackType.MUSIC:
            self.trackProgressBar.configure(value=int(MAXIMUM * state.trackPosition))
            self.playPauseButton.configure(state=NORMAL)
        else:
            self.trackProgressBar.configure(value=0)
            self.playPauseButton.configure(state=DISABLED)

        if state.playbackState is PlaybackState.PLAYING:
            self.playPauseButton.configure(image=self.pause_icon)
        else:
            self.playPauseButton.configure(image=self.play_icon)

        self.__displayTime(state)

    def __displayTime(self, state: PlayerState):
        trackMinutes = int(state.trackLength / 60)
        trackSeconds = state.trackLength % 60

        played = int(state.trackPosition * state.trackLength)
        playedMinutes = int(played / 60)
        playedSeconds = played % 60

        if state.trackType is not TrackType.MUSIC:
            self.timeLabel.configure(text='--:--/--:--')
        else:
            self.timeLabel.configure(text=f'{playedMinutes:02d}:{playedSeconds:02d}/{trackMinutes:02d}:{trackSeconds:02d}')

    def setPlayerController(self, playerController: IPlayerController):
        self.playerController = playerController

        self.volumeScale.configure(command=lambda v: self.__sendVolume())
        self.__sendVolume()

        self.trackProgressBar.bind("<Button-1>", lambda e: self.onProgressBarClicked(e, playerController))
        self.playPauseButton.configure(command=playerController.onPlayPauseClicked)

    def __sendVolume(self):
        if self.playerController is None:
            return

        if self.muted:
            self.playerController.onVolumeSelected(0)
        else:
            self.playerController.onVolumeSelected(self.volumeScale.get())

    def __muteButtonPressed(self):
        self.muted = not self.muted

        if self.muted:
            self.muteButton.configure(image=self.unmute_icon)
        else:
            self.muteButton.configure(image=self.mute_icon)

        self.__sendVolume()



    def onProgressBarClicked(self, event, playerController: IPlayerController):
        percentage = event.x / event.widget.winfo_width()
        playerController.seekTo(percentage)

