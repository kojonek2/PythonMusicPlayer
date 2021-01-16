from Models.Database.Database import Database
from Models.Database.MusicDb import MusicDb
from Models.Database.SkipDb import SkipDb


class SkipService:

    def __init__(self):
        self.__db = Database()

    def getSkipsForMusic(self, path):
        session = self.__db.crateSession()

        music = session.query(MusicDb).join(SkipDb).filter(MusicDb.path == path).first()
        if music is None:
            return None

        skips = list(music.skips)
        session.close()

        return skips

    def addSkipForMusic(self, path, start, end):
        session = self.__db.crateSession()

        music = session.query(MusicDb).join(SkipDb).filter(MusicDb.path == path).first()
        if music is None:
            music = MusicDb(path=path)
            session.add(music)

        skip = SkipDb(start=start, end=end)
        music.skips.append(skip)

        session.commit()
        session.close()

    def deleteSkipsForMusic(self, id):
        session = self.__db.crateSession()

        session.query(SkipDb).filter(SkipDb.id == id).delete()

        session.commit()
        session.close()
