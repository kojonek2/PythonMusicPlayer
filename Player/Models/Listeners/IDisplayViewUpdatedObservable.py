from abc import ABC, abstractmethod

from Models.Listeners.IDisplayViewUpdatedListener import IDisplayViewUpdatedListener


class IDisplayViewUpdatedObservable(ABC):

    @abstractmethod
    def addDisplayViewUpdatedListener(self, listener: IDisplayViewUpdatedListener):
        raise NotImplementedError

    @abstractmethod
    def removeDisplayViewUpdatedListener(self, listener: IDisplayViewUpdatedListener):
        raise NotImplementedError
