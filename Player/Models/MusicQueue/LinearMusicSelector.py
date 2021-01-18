from Models.Database.AlbumDb import AlbumDb
from Models.MusicQueue.AbstractMusicSelector import AbstractMusicSelector, Queue, Position


class LinearMusicSelector(AbstractMusicSelector):

    def nextSelection(self, queue: Queue, selectedPosition: Position) -> Position:
        if len(queue) <= 0:
            return None

        if selectedPosition is None:
            return 0, 0

        if len(queue) <= selectedPosition[0]:
            return 0, 0

        entry = queue[selectedPosition[0]]
        if isinstance(entry, AlbumDb):
            return self.__processAlbum(queue, selectedPosition)
        else:
            return self.__processMusic(queue, selectedPosition)

    def __processMusic(self, queue: Queue, selectedPosition: Position):
        del queue[selectedPosition[0]]
        if len(queue) <= 0:
            return None

        if len(queue) <= selectedPosition[0]:
            return 0, 0

        return selectedPosition[0], 0

    def __processAlbum(self, queue: Queue, selectedPosition: Position):
        album = queue[selectedPosition[0]]

        del album.music[selectedPosition[1]]
        if len(album.music) <= 0:  # whole album played
            del queue[selectedPosition[0]]

            if len(queue) <= 0:
                return None

            if len(queue) <= selectedPosition[0]:
                return 0, 0

            return selectedPosition[0], 0

        else: #tracks left in an album

            if len(album.music) <= selectedPosition[1]:
                return selectedPosition[0], 0

            return selectedPosition
