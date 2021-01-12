from abc import ABC, abstractmethod

from Models.DisplayViewStatus import DisplayViewStatus


class IDisplayViewUpdatedListener(ABC):

    @abstractmethod
    def onDisplayViewUpdated(self, status: DisplayViewStatus):
        raise NotImplementedError
