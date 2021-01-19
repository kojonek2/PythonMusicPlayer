from sqlalchemy import func

from Models.Database.Database import Database
from Models.Database.MusicDb import MusicDb
from datetime import datetime

from Models.Database.PlayEntryDb import PlayEntryDb


class PlayEntryService:

    def __init__(self):
        self.__db = Database()


    def addEntryForMusic(self, path):
        session = self.__db.crateSession()

        music = session.query(MusicDb).filter(MusicDb.path == path).first()
        if music is None:
            music = MusicDb(path=path)
            session.add(music)

        entry = PlayEntryDb(dateTime=datetime.now(), music=music)
        session.add(entry)

        session.commit()
        session.close()

    def getEntriesCountByDay(self):
        session = self.__db.crateSession()

        result = session.query(func.strftime('%w', PlayEntryDb.dateTime), func.count(PlayEntryDb.id)).\
            group_by(func.strftime('%w', PlayEntryDb.dateTime)).all()

        session.close()

        return result

    def getEntriesCountByHour(self):
        session = self.__db.crateSession()

        result = session.query(func.strftime('%H', PlayEntryDb.dateTime), func.count(PlayEntryDb.id)).\
            group_by(func.strftime('%H', PlayEntryDb.dateTime)).all()

        session.close()

        return result
