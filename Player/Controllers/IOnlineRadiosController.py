from abc import ABC, abstractmethod

from Models.RadioStation import RadioStation


class IOnlineRadiosController(ABC):

    @abstractmethod
    def onRadioSelected(self, radio: RadioStation):
        raise NotImplementedError
