from typing import List

class Music:

    def __init__(self, filename, path):
        self.filename: str = filename
        self.path: str = path
        self.skips = None

    def __str__(self):
        return self.filename