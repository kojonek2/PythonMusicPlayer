from tkinter import Frame, Listbox, Scrollbar
from typing import List, Union, Tuple

from Models.Data.Music import Music
from Models.MusicQueue.AlbumEntry import AlbumEntry


class QueuePanel(Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.__initView()

    def __initView(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.queueListBox = Listbox(self)
        self.queueListBox.grid(row=0, column=0, sticky='WENS', padx=(10, 0), pady=10)

        queueScrollbar = Scrollbar(self, command=self.queueListBox.yview)
        queueScrollbar.grid(row=0, column=1, sticky='NS', padx=(0, 10), pady=10)

        self.queueListBox.configure(yscrollcommand=queueScrollbar.set)

        self.queueListBox.bindtags((self.queueListBox, self, "all"))  # disable interaction with listbox

    def displayQueue(self, queue: List[Union[Music, AlbumEntry]], selectionInQueue: Tuple[int, int]):
        self.queueListBox.delete(0, 'end')
        if queue is None:
            return

        selectedIndex = -1

        index = 0
        for i in range(len(queue)):
            entry = queue[i]

            if isinstance(entry, AlbumEntry): #album
                self.queueListBox.insert(index, f'{entry.name}:')
                index += 1

                for j in range(len(entry.music)):
                    if selectionInQueue is not None and selectionInQueue[0] == i:
                        if selectionInQueue[1] == j:
                            selectedIndex = index

                    m = entry.music[j]
                    self.queueListBox.insert(index, f'--> {m.filename}')
                    index += 1

            else: #music
                if selectionInQueue is not None and selectionInQueue[0] == i:
                    selectedIndex = index

                self.queueListBox.insert(index, entry.filename)
                index += 1

        #select played item
        if selectedIndex >= 0:
            self.queueListBox.select_set(selectedIndex)
