from abc import ABC, abstractmethod
from collections import Callable


class IRunnerOnMainThread(ABC):

    @abstractmethod
    def runOnMainThread(self, callable: Callable):
        raise NotImplementedError()