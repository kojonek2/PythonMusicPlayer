from abc import ABC, abstractmethod
from collections import Callable

from Controllers.IAlbumsController import IAlbumsController
from Controllers.IMenuController import IMenuController
from Controllers.IMusicController import IMusicController
from Controllers.IOnlineRadiosController import IOnlineRadiosController
from Controllers.IPlayerController import IPlayerController
from Models.Listeners.IDisplayViewUpdatedListener import IDisplayViewUpdatedListener
from Models.Listeners.IPlayerStateListener import IPlayerStateListener


class IMainWindow(IDisplayViewUpdatedListener, IPlayerStateListener, ABC):

    @abstractmethod
    def mainLoop(self): raise NotImplementedError

    @abstractmethod
    def setMenuController(self, menuController: IMenuController):
        raise NotImplementedError

    @abstractmethod
    def setOnlineRadiosController(self, radioController: IOnlineRadiosController):
        raise NotImplementedError

    @abstractmethod
    def setPlayerController(self, playerController: IPlayerController):
        raise NotImplementedError

    @abstractmethod
    def setMusicController(self, musicController: IMusicController):
        raise NotImplementedError

    @abstractmethod
    def setAlbumsController(self, albumsController: IAlbumsController):
        raise NotImplementedError

    @abstractmethod
    def runOnEventLoop(self, callable: Callable):
        raise NotImplementedError