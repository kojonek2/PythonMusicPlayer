

class Music:

    def __init__(self, filename, path):
        self.filename: str = filename
        self.path: str = path

    def __str__(self):
        return self.filename