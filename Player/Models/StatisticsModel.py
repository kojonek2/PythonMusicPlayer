import os

from Models.Data.PlotData import PlotData
from Models.Data.Statistics import Statistics
from Models.DisplayViewStatus import DisplayViewStatus
from Models.Services.AlbumService import AlbumService
from Models.Services.PlayEntryService import PlayEntryService

WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
HOURS = [i for i in range(25)]


class StatisticsModel:

    def fillStatistics(self, displayViewStatus: DisplayViewStatus):
        statistics = Statistics()
        statistics.playsByWeekday = self.__getPlaysByWeekdayData()
        statistics.playsByHour = self.__getPlaysByHoursData()
        statistics.musicUsageInAlbums = self.__getTopMusicUsagesInAlbums()

        displayViewStatus.statistics = statistics

    def __getPlaysByWeekdayData(self):
        values = [0]*len(WEEKDAYS)

        playEntryService = PlayEntryService()
        groups = playEntryService.getEntriesCountByDay()

        for group in groups:
            weekdayIndex = int(group[0])
            count = int(group[1])
            values[weekdayIndex] = count

        return PlotData(WEEKDAYS, values)

    def __getPlaysByHoursData(self):
        values = [0]*len(HOURS)

        playEntryService = PlayEntryService()
        groups = playEntryService.getEntriesCountByHour()

        for group in groups:
            hourIndex = int(group[0])
            count = int(group[1])
            values[hourIndex] = count

        return PlotData(HOURS, values)

    def __getTopMusicUsagesInAlbums(self):
        categories = []
        values = []

        albumService = AlbumService()
        groups = albumService.getTopMusicUsagesInAlbums()

        for group in groups:
            filename = os.path.basename(group[0])
            count = int(group[1])

            categories.append(filename)
            values.append(count)

        return PlotData(categories, values)
