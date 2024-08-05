import numpy as np
import random
import os
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
sprint_1_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(sprint_1_directory)

from wdc.coverage.args_formatter import Formatting
from wdc.coverage.coverage import Coverage

class AverageCoverage(Coverage):
    # initial values to use for coverages
    basic_subset = ["ansi(\"2015-01-01\",\"2015-05-01\")", 
                    "Lat(-90,90)",
                    "Lon(-180,180)"]
        
    def __init__(self, coverage_name, subsets = basic_subset, index = None):
        Coverage.__init__(self, coverage_name, index)
        self.subsets = subsets
    
    @staticmethod  
    def subset_formatter(year1:str, month1:str, day1:str, 
                         Lat1:int, Lon1:int, 
                         year2:str = None, month2:str = None,
                         day2:str = None, Lat2:int = None, 
                         Lon2:int = None ):
        '''
        Method for forming subsets for coverages from S2 class

        Args:
        year1, month1, day1: for initial date 
        Lat1: for initial latitude coordinate
        Lon1: for initial longitude coordinate
        year2, month2, day2: (optional) for upper bound date, if trimming is wanted
        Lat2: (optional)  for upper bound latitude coordinate, if trimming is wanted
        Lon2: (optional) for upper bound longitude coordinate, if trimming is wanted

        Returns: 
        subsets (list): list containing the ansi, Lat, Lon formatted, ready to be sent to request
        '''
        if year2 is None:
            ansi = Formatting.ansi_sliceformat(year1, month1, day1)
        else:
            ansi = Formatting.ansi_trimformat(year1, month1, day1, 
                                              year2, month2, day2)
        if Lat2 is None:
            Lat = Formatting.Lat_sliceformat(Lat1)
        else:
            Lat = Formatting.Lat_trimformat(Lat1, Lat2)

        if Lon2 is None:
            Lon = Formatting.Lon_sliceformat(Lon1)
        else:
            Lon = Formatting.Lon_trimformat(Lon1, Lon2)
        
        subsets = [ansi, Lat, Lon]
        return subsets
    
    @staticmethod
    def randomize_coverage():
        '''
        Static method for taking a random ID of an Average coverage and random subsets of descriptive coverage values
        
        Return:
            name (str): coverage ID from the list of possible IDs
            subsets (list): list of formatted subsets of the ansi, Lat, Lon axis
        '''
        # all IDs of coverages of subtype Average
        IDs = [ "AverageChloroColor",
                "AverageChloroColorScaled",	
                "AverageChloroColor_16",
                "AverageChloroColor_2",
                "AverageChloroColor_32",	
                "AverageChloroColor_4",
                "AverageChloroColor_64",
                "AverageChloroColor_8",
                "AvgLandTemp",
                "AvgTemperatureColor",
                "AvgTemperatureColorScaled",
                "AvgTemperatureColor_16",
                "AvgTemperatureColor_32",
                "AvgTemperatureColor_4",
                "AvgTemperatureColor_64",
                "AvgTemperatureColor_8"]
    
        ["ansi(\"2015-01-01\",\"2015-05-01\")", 
                    "Lat(-90,90)",
                    "Lon(-180,180)"]
    
        # values for ansi, Lat, Lon
        year = "2015"
        months = ["01", "02", "03", "04"]
        days = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", 
                "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", 
                "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
        Lats = np.arange(-90, 91)
        Lons = np.arange(-180, 181)
        
        # pick random id
        name = random.choice(IDs)

        # pick random ansi
        # the dates need to make sense chronologically
        year1 = year
        year2 = year
        month1 = random.choice(months)
        month2 = random.choice(months)
        while  months.index(month2) < months.index(month1)  :
            month2 = random.choice(months)
        day1 = random.choice(days)
        day2 = random.choice(days)
        if month1 == month2:
            while  days.index(day2) < days.index(day1)  :
                day2 = random.choice(days)
            # check if values are the same
                # then slice instead of trim
            if day1 == day2:
                day2 = None
                year2 = None
                month2 = None
        
        # pick random Lat
        la1 = random.choice(Lats)
        la2 = random.randint(la1, 90)
        # check if values are the same
            # then slice instead of trim
        if la1 == la2:
            la2 = None
        
        # pick random Lon
        lo1 = random.choice(Lons)
        lo2 = random.randint(lo1, 180)
        # check if values are the same
            # then slice instead of trim
        if lo1 == lo2:
            lo2 = None
    
        # create subsets
        subsets = AverageCoverage.subset_formatter(year1, month1, day1,
                                                la1, lo1, year2, month2,
                                                day2, la2, lo2)
        
        return name, subsets
        # example returns 
        # name = "AvgTemperatureColor_32"
        # subsets = ['ansi("2015-01-26","2015-04-06")', 'Lat(21,25)', 'Lon(-44,126)']  
    
