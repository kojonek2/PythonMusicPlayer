from tkinter import Frame, Label, TOP, BOTH
from tkinter.ttk import Notebook

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Models.Data.Statistics import Statistics

import numpy as np


PLAYS_BY_WEEKDAY = 'Music played by weekday'
PLAYS_BY_HOUR = 'Music played by hours'
TOP_MUSIC_USAGE_IN_ALBUMS = 'Top music usage in albums'

class StatisticsPanel(Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.__initView()

    def __initView(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        tabControl = Notebook(self)
        tabControl.grid(row=0, column=0, sticky='NSWE')

        #################################################################################################

        self.playsByWeekdayFrame = Frame(tabControl)
        self.playsByWeekdayFrame.grid_columnconfigure(0, weight=1)
        self.playsByWeekdayFrame.grid_rowconfigure(0, weight=1)
        tabControl.add(self.playsByWeekdayFrame, text=PLAYS_BY_WEEKDAY)

        #################################################################################################

        self.playsByHourFrame = Frame(tabControl)
        self.playsByHourFrame.grid_columnconfigure(0, weight=1)
        self.playsByHourFrame.grid_rowconfigure(0, weight=1)
        tabControl.add(self.playsByHourFrame, text=PLAYS_BY_HOUR)

        #################################################################################################

        self.topMusicUsageInAlbumFrame = Frame(tabControl)
        self.topMusicUsageInAlbumFrame.grid_columnconfigure(0, weight=1)
        self.topMusicUsageInAlbumFrame.grid_rowconfigure(0, weight=1)
        tabControl.add(self.topMusicUsageInAlbumFrame, text=TOP_MUSIC_USAGE_IN_ALBUMS)


    def displayStatistics(self, statistics: Statistics):
        self.__attachPlaysByWeekDay(statistics.playsByWeekday.categories, statistics.playsByWeekday.values)
        self.__attachPlaysByHour(statistics.playsByHour.categories, statistics.playsByHour.values)
        self.__attachTopMusicUsage(statistics.musicUsageInAlbums.categories, statistics.musicUsageInAlbums.values)

    def __attachPlaysByWeekDay(self, categories, values):
        for widget in self.playsByWeekdayFrame.grid_slaves():
            widget.grid_forget()

        fig = Figure(figsize=(5,4), dpi=100)
        fig.add_subplot(111).bar(categories, values)

        canvas = FigureCanvasTkAgg(fig, master=self.playsByWeekdayFrame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky='NSWE')

    def __attachPlaysByHour(self, categories, values):
        for widget in self.playsByHourFrame.grid_slaves():
            widget.grid_forget()

        fig = Figure(figsize=(5,4), dpi=100)
        subplot = fig.add_subplot(111)
        subplot.bar(categories, values)
        subplot.set_xlim([-1, 24])

        canvas = FigureCanvasTkAgg(fig, master=self.playsByHourFrame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky='NSWE')

    def __attachTopMusicUsage(self, categories, values):
        for widget in self.topMusicUsageInAlbumFrame.grid_slaves():
            widget.grid_forget()

        fig = Figure(figsize=(5,4), dpi=100)
        subplot = fig.add_subplot(111)
        bar_plot = subplot.bar([i + 1 for i in range(len(categories))], values)

        for idx, rect in enumerate(bar_plot):
            height = rect.get_height()
            subplot.text(rect.get_x() + rect.get_width() / 2., 0.1,
                    categories[idx],
                    ha='center', va='bottom', rotation=90)

        canvas = FigureCanvasTkAgg(fig, master=self.topMusicUsageInAlbumFrame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky='NSWE')

