from typing import List

from Models.Data.Music import Music


class AlbumEntry:

    def __init__(self, name):
        self.name = name
        self.music: List[Music] = []