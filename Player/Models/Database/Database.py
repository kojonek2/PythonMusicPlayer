from sphinxcontrib.websupport.storage.sqlalchemy_db import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()


class Database:
    __engine = None
    __scoped_sesion = None

    def __init__(self):
        if Database.__engine is None:
            Database.__engine = create_engine('sqlite:///database.db')
            Base.metadata.create_all(Database.__engine)

        if Database.__scoped_sesion is None:
            Database.__scoped_sesion = scoped_session(sessionmaker(bind=Database.__engine))

    def crateSession(self) -> Session:
        return Database.__scoped_sesion()
