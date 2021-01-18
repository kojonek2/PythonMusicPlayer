from Models.MusicQueue.AbstractMusicSelector import AbstractMusicSelector, Queue, Position
from Models.MusicQueue.AlbumEntry import AlbumEntry
from random import randint


class RandomMusicSelector(AbstractMusicSelector):

    def nextSelection(self, queue: Queue, selectedPosition: Position) -> Position:
        if len(queue) <= 0:
            return None

        self.__deletePlayedEntry(queue, selectedPosition)

        if len(queue) <= 0:
            return None

        count = self.__musicCount(queue)
        random = randint(0, count - 1)

        index = 0
        for i in range(len(queue)):
            entry = queue[i]

            if isinstance(entry, AlbumEntry): # album
                if random >= index + len(entry.music): #random is not in this album
                    index += len(entry.music)

                else: #random in this album
                    return i, random - index

            else: # music
                if index == random:
                    return i, 0
                index += 1

        return None

    def __musicCount(self, queue: Queue):
        count = 0

        for entry in queue:
            if isinstance(entry, AlbumEntry):
                count += len(entry.music)
            else:
                count += 1

        return count

    def __deletePlayedEntry(self, queue: Queue, selectedPosition: Position):
        if selectedPosition is not None:
            entry = queue[selectedPosition[0]]
            if isinstance(entry, AlbumEntry):
                del entry.music[selectedPosition[1]]
                if len(entry.music) <= 0:  # whole album played
                    del queue[selectedPosition[0]]

            else:
                del queue[selectedPosition[0]]