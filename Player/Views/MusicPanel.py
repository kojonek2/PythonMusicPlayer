from tkinter import Frame, Listbox, Scrollbar
from typing import List


from Controllers.IMusicController import IMusicController
from Models.Music import Music


class MusicPanel(Frame):

    def __init__(self, parent, musicController: IMusicController):
        super().__init__(parent)
        self.musicController = musicController
        self.musicList: List[Music] = []

        self.__initView()

    def __initView(self):
        self.grid_columnconfigure(0, weight=1)

        self.musicListBox = Listbox(self)
        self.musicListBox.grid(row=0, column=0, sticky='WE', padx=(10, 0), pady=10)
        self.musicListBox.bind('<Double-1>', self.musicDoubleClicked)

        scrollbar = Scrollbar(self, command=self.musicListBox.yview)
        scrollbar.grid(row=0, column=1, sticky='NS', padx=(0, 10), pady=10)

        self.musicListBox.configure(yscrollcommand=scrollbar.set)

    def displayMusic(self, music: List[Music]):
        self.musicList = music
        self.musicListBox.delete(0, 'end')
        for i in range(len(music)):
            m = music[i]
            self.musicListBox.insert(i, m)

    def musicDoubleClicked(self, event):
        music = self.musicList[self.musicListBox.curselection()[0]]
        self.musicController.onMusicDoubleClicked(music)