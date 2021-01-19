from Models.Data.PlotData import PlotData


class Statistics:

    def __init__(self):
        self.playsByWeekday: PlotData = None
        self.playsByHour: PlotData = None
        self.musicUsageInAlbums: PlotData = None