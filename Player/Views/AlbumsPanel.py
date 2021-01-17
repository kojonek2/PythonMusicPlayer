import os
from tkinter import Frame, Label, Listbox, Scrollbar, Button, Entry, messagebox, END
from typing import List

from Controllers.IAlbumsController import IAlbumsController
from Models.Data.Music import Music
from Models.Database.AlbumDb import AlbumDb

ALBUM_DELETE_TEXT = 'Delete album'
ALBUM_EXPORT_TEXT = 'Export album'
ALBUM_IMPORT_TEXT = 'Import album'
ALBUM_CREATE_LABEL_TEXT = 'Create album with name:'
ALBUM_CREATE_BUTTON_TEXT = 'Create album'

MUSIC_ON_COMPUTER_TEXT = 'Music on computer:'
MUSIC_IN_ALBUM_TEXT = 'Music in album:'

DELETE_ALBUM_SELECT_TEXT = 'Select album firstly!'
EXPORT_ALBUM_SELECT_TEXT = 'Select album firstly!'
CRATE_ALBUM_INSERT_NAME_TEXT = 'Insert name of album firstly!'
ADD_TO_ALBUM_SELECT_TEXT = 'Select music to add firstly!'
REMOVE_FROM_ALBUM_SELECT_TEXT = 'Select music to remove firstly!'

class AlbumsPanel(Frame):

    def __init__(self, parent, albumsController: IAlbumsController):
        super().__init__(parent)
        self.albumsController = albumsController

        self.albumList: List[AlbumDb] = []
        self.selectedAlbumName: str = None

        self.musicFromDisc: List[Music] = []

        self.displayedMusicOnComputer = None
        self.displayedMusicInAlbum = None

        self.__initView()

    def __initView(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.albumsListBox = Listbox(self, exportselection=0)
        self.albumsListBox.grid(row=0, column=0, sticky='WE', padx=(10, 0), pady=10)
        #self.albumsListBox.bind('<Double-1>', self.musicDoubleClicked) # TODO
        self.albumsListBox.bind("<<ListboxSelect>>", self.__albumSelected)

        albumsScrollbar = Scrollbar(self, command=self.albumsListBox.yview)
        albumsScrollbar.grid(row=0, column=1, sticky='NS', padx=(0, 10), pady=10)

        self.albumsListBox.configure(yscrollcommand=albumsScrollbar.set)

        ######################################################################################################

        buttonsFrame = Frame(self)
        buttonsFrame.grid(row=1, column=0, sticky='W', padx=10)

        self.albumDeleteButton = Button(buttonsFrame, text=ALBUM_DELETE_TEXT, command=self.__deleteAlbum)
        self.albumDeleteButton.grid(row=0, column=0, padx=5)

        self.albumExportButton = Button(buttonsFrame, text=ALBUM_EXPORT_TEXT, command=self.__exportAlbumClicked)
        self.albumExportButton.grid(row=0, column=1, padx=5)

        self.albumImportButton = Button(buttonsFrame, text=ALBUM_IMPORT_TEXT, command=self.__importAlbumClicked)
        self.albumImportButton.grid(row=0, column=2, padx=5)

        ######################################################################################################

        createFrame = Frame(self)
        createFrame.grid(row=2, column=0, sticky='W', padx=10)

        label = Label(createFrame, text=ALBUM_CREATE_LABEL_TEXT)
        label.grid(row=0, column=0)

        self.createAlbumNameEntry = Entry(createFrame)
        self.createAlbumNameEntry.grid(row=0, column=1)

        self.createAlbumButton = Button(createFrame, text=ALBUM_CREATE_BUTTON_TEXT, command=self.__createAlbum)
        self.createAlbumButton.grid(row=0, column=2)

        ######################################################################################################
        # Music on computer

        musicFrame = Frame(self, padx=10, pady=10)
        musicFrame.grid(row=3, column=0, columnspan=2, sticky='WENS')
        musicFrame.grid_columnconfigure(0, weight=1)
        musicFrame.grid_columnconfigure(3, weight=1)
        musicFrame.grid_rowconfigure(1, weight=1)

        label = Label(musicFrame, text=MUSIC_ON_COMPUTER_TEXT)
        label.grid(row=0, column=0, sticky='W')

        self.musicOnComputerListBox = Listbox(musicFrame)
        self.musicOnComputerListBox.grid(row=1, column=0, sticky='WENS')

        musicOnComputerScrollbar = Scrollbar(musicFrame, command=self.musicOnComputerListBox.yview)
        musicOnComputerScrollbar.grid(row=1, column=1, sticky='NS')

        self.musicOnComputerListBox.configure(yscrollcommand=musicOnComputerScrollbar.set)

        ######################################################################################################

        buttonFrame = Frame(musicFrame, padx=10)
        buttonFrame.grid(row=1, column=2)

        self.removeFromAlbumButton = Button(buttonFrame, text='<<', command=self.__removeMusicFromAlbumClicked)
        self.removeFromAlbumButton.grid(row=0, column=0)

        self.addToAlbumButton = Button(buttonFrame, text='>>', command=self.__addMusicToAlbumClicked)
        self.addToAlbumButton.grid(row=1, column=0)

        ######################################################################################################
        #Music in album

        label = Label(musicFrame, text=MUSIC_IN_ALBUM_TEXT)
        label.grid(row=0, column=3, sticky='W')

        self.musicInAlbumListBox = Listbox(musicFrame)
        self.musicInAlbumListBox.grid(row=1, column=3, sticky='WENS')

        musicInAlbumScrollbar = Scrollbar(musicFrame, command=self.musicInAlbumListBox.yview)
        musicInAlbumScrollbar.grid(row=1, column=4, sticky='NS')

        self.musicInAlbumListBox.configure(yscrollcommand=musicInAlbumScrollbar.set)

        ######################################################################################################

    def displayAlbums(self, albums: List[AlbumDb], musicFromDisc: List[Music]):
        self.albumList = albums
        self.musicFromDisc = musicFromDisc

        self.albumsListBox.delete(0, 'end')
        for i in range(len(self.albumList)):
            a = self.albumList[i]
            self.albumsListBox.insert(i, a.name)

        if self.selectedAlbumName is not None:
            selectedIndex = -1
            for i in range(len(self.albumList)):
                if self.albumList[i].name == self.selectedAlbumName:
                    selectedIndex = i
                    break

            if selectedIndex >= 0:
                self.albumsListBox.select_set(selectedIndex)
                self.albumsListBox.event_generate("<<ListboxSelect>>")

    def __deleteAlbum(self):
        selection = self.albumsListBox.curselection()

        if len(selection) <= 0:
            messagebox.showwarning('Warning', DELETE_ALBUM_SELECT_TEXT)
            return

        self.albumsListBox.selection_clear(0, END)
        self.albumsListBox.event_generate("<<ListboxSelect>>")

        album = self.albumList[selection[0]]
        self.albumsController.deleteAlbum(album.name)

    def __createAlbum(self):
        name = self.createAlbumNameEntry.get()

        if name is None or name == '':
            messagebox.showwarning('Warning', CRATE_ALBUM_INSERT_NAME_TEXT)
            return

        self.albumsController.createAlbum(name)

    def __albumSelected(self, event):
        self.musicOnComputerListBox.delete(0, 'end')
        self.musicInAlbumListBox.delete(0, 'end')

        selection = self.albumsListBox.curselection()
        if len(selection) <= 0:
            return

        selectedAlbum = self.albumList[selection[0]]
        self.selectedAlbumName = selectedAlbum.name

        self.__lisMusicOnComputer(selectedAlbum)
        self.__lisMusicInAlbum(selectedAlbum)

    def __lisMusicOnComputer(self, album):
        musicInAlbum = set()
        for m in album.music:
            musicInAlbum.add(m.path)

        if self.musicFromDisc is None:
            return

        music = self.musicFromDisc.copy()
        music = filter(lambda m: m.path not in musicInAlbum, music)
        self.displayedMusicOnComputer = list(music)

        i = 0
        for m in self.displayedMusicOnComputer:
            self.musicOnComputerListBox.insert(i, m.filename)
            i = i + 1

    def __lisMusicInAlbum(self, album):
        musicOnDisc = set()
        if self.musicFromDisc is not None:
            for m in self.musicFromDisc:
                musicOnDisc.add(m.path)

        self.displayedMusicInAlbum = list(album.music)

        i = 0
        for m in self.displayedMusicInAlbum:
            description = os.path.basename(m.path)
            if m.path not in musicOnDisc:
                description = '<missing> ' + m.path

            self.musicInAlbumListBox.insert(i, description)
            i = i + 1

    def __addMusicToAlbumClicked(self):
        selection = self.albumsListBox.curselection()
        if len(selection) <= 0:
            return

        selectedAlbum = self.albumList[selection[0]]

        selection = self.musicOnComputerListBox.curselection()
        if len(selection) <= 0:
            messagebox.showwarning('Warning', ADD_TO_ALBUM_SELECT_TEXT)
            return

        selectedMusic = self.displayedMusicOnComputer[selection[0]]

        self.albumsController.addMusicToAlbum(selectedAlbum.name, selectedMusic.path)

    def __removeMusicFromAlbumClicked(self):
        selection = self.albumsListBox.curselection()
        if len(selection) <= 0:
            return

        selectedAlbum = self.albumList[selection[0]]

        selection = self.musicInAlbumListBox.curselection()
        if len(selection) <= 0:
            messagebox.showwarning('Warning', REMOVE_FROM_ALBUM_SELECT_TEXT)
            return

        selectedMusic = self.displayedMusicInAlbum[selection[0]]

        self.albumsController.removeMusicFromAlbum(selectedAlbum.name, selectedMusic.path)

    def __exportAlbumClicked(self):
        selection = self.albumsListBox.curselection()
        if len(selection) <= 0:
            messagebox.showwarning('Warning', EXPORT_ALBUM_SELECT_TEXT)
            return

        selectedAlbum = self.albumList[selection[0]]
        self.albumsController.exportAlbum(selectedAlbum.name)

    def __importAlbumClicked(self):
        self.albumsController.importAlbum()