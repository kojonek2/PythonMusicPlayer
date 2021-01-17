import os
import zipfile
from zipfile import ZipFile, ZIP_DEFLATED

from Models.Services.AlbumService import AlbumService

from win32com.shell import shell, shellcon

import json

NAME_KEY = 'name'
PATHS_KEY = 'paths'
DESCRIPTION_KEY = 'description'

class SerializationModel:

    def exportAlbum(self, name, filename):
        albumService = AlbumService()

        album = albumService.getAlbum(name)
        if album is None:
            return

        with ZipFile(filename, 'w', ZIP_DEFLATED) as zipFile:

            musicFolder = shell.SHGetFolderPath(0, shellcon.CSIDL_MYMUSIC, None, 0)

            for m in album.music:
                path = os.path.join(musicFolder, m.path)
                if os.path.isfile(path):
                    zipFile.write(path, m.path)

            description = self.__createDescriptionForAblum(album)
            zipFile.writestr(DESCRIPTION_KEY, description)

    def __createDescriptionForAblum(self, album):
        musicPaths = []
        for m in album.music:
            musicPaths.append(m.path)

        description = {
            NAME_KEY: album.name,
            PATHS_KEY: musicPaths
        }

        return json.dumps(description)

    def importAlbum(self, filename):
        try:
            albumService = AlbumService()

            with ZipFile(filename, 'r', ZIP_DEFLATED) as zipFile:
                if DESCRIPTION_KEY not in zipFile.namelist():
                    return False

                description = json.loads(zipFile.read(DESCRIPTION_KEY))
                if NAME_KEY not in description or PATHS_KEY not in description:
                    return False

                albumName = description[NAME_KEY]
                album = albumService.getAlbum(albumName)
                if album is not None:
                    return True # album is already present

                musicFolder = shell.SHGetFolderPath(0, shellcon.CSIDL_MYMUSIC, None, 0)
                albumService.createAlbum(albumName)
                for path in description[PATHS_KEY]:
                    albumService.addMusic(albumName, path)

                    forwardSlashPath = path.strip('.\\').replace('\\', '/')
                    if forwardSlashPath in zipFile.namelist():
                        absolutePath = os.path.join(musicFolder, path)
                        if not os.path.exists(absolutePath):
                            zipFile.extract(forwardSlashPath, musicFolder)

            return True
        except:
            return False
