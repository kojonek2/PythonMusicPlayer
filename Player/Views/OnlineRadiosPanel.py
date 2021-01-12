from tkinter import Frame, Label, Button
from typing import List
from PIL import Image
from PIL.ImageTk import PhotoImage

from Controllers.IOnlineRadiosController import IOnlineRadiosController
from Models.RadioStation import RadioStation
from Views.ScrollableFrame import ScrollableFrame

NO_RADIOS_TEXT = 'No radio stations found!'
ENTRY_HEIGHT = 200
ICONS_SIZE = 128
ROWS = 4


class OnlineRadiosPanel(ScrollableFrame):

    def __init__(self, parent, radioController: IOnlineRadiosController):
        super().__init__(parent)

        self.icons: List[PhotoImage] = []
        self.radioController = radioController

        self.__initView()

    def __initView(self):
        for i in range(ROWS):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)

    def displayRadios(self, radios: List[RadioStation]):
        if radios is None or len(radios) <= 0:
            label = Label(self.scrollable_frame, text=NO_RADIOS_TEXT)
            label.grid(row=0, column=0, columnspan=4)
            return

        self.icons.clear()
        for i in range(len(radios)):
            radio = radios[i]
            column = i % ROWS
            row = int(i / ROWS)

            frame = Frame(self.scrollable_frame, height=ENTRY_HEIGHT)
            frame.grid(row=row, column=column, sticky='NSWE', padx=10, pady=10)
            frame.propagate(False)

            image = Image.open(radio.pathToImage)
            image = image.resize((ICONS_SIZE, ICONS_SIZE), Image.ANTIALIAS)
            self.icons.append(PhotoImage(image=image))
            iconLabel = Label(frame, image=self.icons[-1])
            iconLabel.pack()

            nameLabel = Label(frame, text=radio.name, font=('Arial', 20))
            nameLabel.pack()

            self.__bindWithChildren(frame, lambda e, r=radio: self.radioController.onRadioSelected(r))

    def __bindWithChildren(self, widget, callable):
        widget.bind('<Double-Button-1>', callable)
        for child in widget.slaves():
            self.__bindWithChildren(child, callable)