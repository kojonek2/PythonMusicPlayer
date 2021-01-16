from tkinter import Frame, Listbox, Scrollbar, Label, Button, Entry, messagebox, END
from typing import List


from Controllers.IMusicController import IMusicController
from Models.Data.Music import Music

SKIP_TEXT = 'Fragments to skip:'
DELETE_SKIP_TEXT = 'Delete fragment to skip'
ADD_SKIP_LABEL_TEXT = 'Add fragment skip from:'
ADD_SKIP_TO_LABEL_TEXT = 'to'
ADD_SKIP_BUTTON_TEXT = 'Add'

ADD_SKIP_END_LOWER_THAN_START = 'Skip times improper! From has to be before to time!'
ADD_SKIP_SELECT_MUSIC = 'Please select music firstly!'
ADD_SKIP_PARSE_ERROR_TEXT = 'Use only numbers to enter skip times'

DELETE_SKIP_SELECT_MUSIC = 'Please select fragment to skip firstly!'

class MusicPanel(Frame):

    def __init__(self, parent, musicController: IMusicController):
        super().__init__(parent)
        self.musicController = musicController
        self.musicList: List[Music] = []

        self.selectedMusicPath: str = None

        self.__initView()

    def __initView(self):
        self.grid_columnconfigure(0, weight=1)

        self.musicListBox = Listbox(self)
        self.musicListBox.grid(row=0, column=0, sticky='WE', padx=(10, 0), pady=10)
        self.musicListBox.bind('<Double-1>', self.musicDoubleClicked)
        self.musicListBox.bind("<<ListboxSelect>>", self.musicSelected)

        musicScrollbar = Scrollbar(self, command=self.musicListBox.yview)
        musicScrollbar.grid(row=0, column=1, sticky='NS', padx=(0, 10), pady=10)

        self.musicListBox.configure(yscrollcommand=musicScrollbar.set)

        ################################################################################

        skipLabel = Label(self, text=SKIP_TEXT)
        skipLabel.grid(row=1, column=0)

        self.skipListBox = Listbox(self, exportselection=0)
        self.skipListBox.grid(row=2, column=0, sticky='WE', padx=(10, 0), pady=10)

        skipScrollbar = Scrollbar(self, command=self.skipListBox.yview)
        skipScrollbar.grid(row=2, column=1, sticky='NS', padx=(0, 10), pady=10)

        self.skipListBox.configure(yscrollcommand=skipScrollbar.set)

        self.deleteSkipButton = Button(self, text=DELETE_SKIP_TEXT, command=self.onSkipDelete)
        self.deleteSkipButton.grid(row=3, column=0, sticky='W', padx=10)

        ################################################################################

        self.addSkipFrame = Frame(self)
        self.addSkipFrame.grid(row=4, column=0, padx=10, sticky='W')

        self.addSkipLabel = Label(self.addSkipFrame, text=ADD_SKIP_LABEL_TEXT)
        self.addSkipLabel.grid(row=0, column=0)

        self.addSkipStartMinutesTE = Entry(self.addSkipFrame, width=5, exportselection=0)
        self.addSkipStartMinutesTE.insert(END, '0')
        self.addSkipStartMinutesTE.grid(row=0, column=1)

        label = Label(self.addSkipFrame, text=':')
        label.grid(row=0, column=2)

        self.addSkipStartSecondsTE = Entry(self.addSkipFrame, width=5, exportselection=0)
        self.addSkipStartSecondsTE.insert(END, '0')
        self.addSkipStartSecondsTE.grid(row=0, column=3)

        label = Label(self.addSkipFrame, text=ADD_SKIP_TO_LABEL_TEXT)
        label.grid(row=0, column=4)

        self.addSkipEndMinutesTE = Entry(self.addSkipFrame, width=5, exportselection=0)
        self.addSkipEndMinutesTE.insert(END, '0')
        self.addSkipEndMinutesTE.grid(row=0, column=5)

        label = Label(self.addSkipFrame, text=':')
        label.grid(row=0, column=6)

        self.addSkipEndSecondsTE = Entry(self.addSkipFrame, width=5, exportselection=0)
        self.addSkipEndSecondsTE.insert(END, '0')
        self.addSkipEndSecondsTE.grid(row=0, column=7)

        self.addSkipButton = Button(self.addSkipFrame, text=ADD_SKIP_BUTTON_TEXT, command=self.__addSkip)
        self.addSkipButton.grid(row=0, column=8, padx=2)

    def displayMusic(self, music: List[Music]):
        self.musicList = music

        self.musicListBox.delete(0, 'end')
        for i in range(len(music)):
            m = music[i]
            self.musicListBox.insert(i, m)

        if self.selectedMusicPath is not None:
            selectedIndex = -1
            for i in range(len(self.musicList)):
                if self.musicList[i].path == self.selectedMusicPath:
                    selectedIndex = i
                    break

            if selectedIndex >= 0:
                self.musicListBox.select_set(selectedIndex)
                self.musicListBox.event_generate("<<ListboxSelect>>")

    def musicDoubleClicked(self, event):
        music = self.musicList[self.musicListBox.curselection()[0]]
        self.musicController.onMusicDoubleClicked(music)

    def onSkipDelete(self):
        musicSelection = self.musicListBox.curselection()
        skipSelection = self.skipListBox.curselection()

        if len(skipSelection) <= 0 or len(musicSelection) <= 0:
            messagebox.showwarning('Warning', DELETE_SKIP_SELECT_MUSIC)
            return

        music = self.musicList[musicSelection[0]]
        self.musicController.onSkipDeleteClicked(music.skips[skipSelection[0]])

    def musicSelected(self, event):
        self.skipListBox.delete(0, 'end')

        selection = self.musicListBox.curselection()
        if len(selection) <= 0:
            return

        selectedMusic = self.musicList[selection[0]]
        self.selectedMusicPath = selectedMusic.path

        if selectedMusic.skips is not None:
            for i in range(len(selectedMusic.skips)):
                s = selectedMusic.skips[i]

                startMinute = int(s.start / 60)
                startSecond = s.start % 60
                stopMinute = int(s.end / 60)
                stopSecond = s.end % 60

                text = f'Skip from {startMinute:02d}:{startSecond:02d} to {stopMinute:02d}:{stopSecond:02d}'
                self.skipListBox.insert(i, text)

    def __addSkip(self):
        selection = self.musicListBox.curselection()

        if len(selection) <= 0:
            messagebox.showwarning('Warning', ADD_SKIP_SELECT_MUSIC)
            return

        music = self.musicList[selection[0]]

        try:
            startMinutes = int(self.addSkipStartMinutesTE.get())
            startSeconds = int(self.addSkipStartSecondsTE.get())
            endMinutes = int(self.addSkipEndMinutesTE.get())
            endSeconds = int(self.addSkipEndSecondsTE.get())
        except:
            messagebox.showwarning('Warning', ADD_SKIP_PARSE_ERROR_TEXT)
            return

        start = startMinutes * 60 + startSeconds
        end = endMinutes * 60 + endSeconds

        if end <= start:
            messagebox.showwarning('Warning', ADD_SKIP_END_LOWER_THAN_START)
            return

        self.musicController.onSkipAddClicked(music.path, start, end)
