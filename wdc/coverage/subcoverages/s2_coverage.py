import numpy as np
import random
import os
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
sprint_1_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(sprint_1_directory)

from wdc.coverage.args_formatter import Formatting
from wdc.coverage.coverage import Coverage

class S2Coverage(Coverage):

    # initial values to use for coverages
    basic_subset = ["ansi(\"2021-04-08\",\"2021-04-10\")", 
                    "E(669960,729960)",
                    "N(4990200,5015220)"]
    
    def __init__(self, coverage_name, subsets = basic_subset, index = None):
        Coverage.__init__(self, coverage_name, index)
        self.subsets = subsets
    
    @staticmethod  
    def subset_formatter(year1:str, month1:str, day1:str, 
                         e1:int, n1:int, 
                         year2:str = None, month2:str = None,
                         day2:str = None, e2:int = None, 
                         n2:int = None ):
        ''' 
        Static method for formatting subsets for coverages from S2 class

        Args:
        year1, month1, day1: for initial date 
        e1: for initial E coordinate
        n1: for initial N coordinate
        year2, month2, day2: (optional) for upper bound date, if trimming is wanted
        e2: (optional)  for upper bound E coordinate, if trimming is wanted
        n2: (optional) for upper bound E coordinate, if trimming is wanted

        Returns: 
        subsets is a list containing the ansi, E, N formatted, ready to be sent to request
        '''
        if year2 is None:
            ansi = Formatting.ansi_sliceformat(year1, month1, day1)
        else:
            ansi = Formatting.ansi_trimformat(year1, month1, day1, 
                                              year2, month2, day2)
        if e2 is None:
            E = Formatting.E_sliceformat(e1)
        else:
            E = Formatting.E_trimformat(e1, e2)

        if n2 is None:
            N = Formatting.N_sliceformat(n1)
        else:
            N = Formatting.N_trimformat(n1, n2)
        
        subsets = [ansi, E, N]
        return subsets
    
    @staticmethod
    def randomize_coverage():
        '''
        Static method for taking a random ID of an S2 coverage and random subsets of descriptive coverage values
        
        Return:
            name (str): coverage ID from the list of possible IDs
            subsets (list): list of formatted subsets of the ansi, E, N axis
        '''
        # all IDs of coverages of subtype S2
        IDs = [ "S2_L2A_32631_B01_60m",
                "S2_L2A_32631_B03_10m",	
                "S2_L2A_32631_B04_10m",
                "S2_L2A_32631_B08_10m",
                "S2_L2A_32631_B12_20m",	
                "S2_L2A_32631_TCI_60m"]
    
        # values for ansi, E, N
        year = "2021"
        month = "04"
        days = ["08", "09", "10"]
        Es = np.arange(669960, 729961)
        Ns = np.arange(4990200, 5015221)
        
        # pick random id
        name = random.choice(IDs)

        # pick random ansi
        # the dates need to make sense chronologically
        year1 = year
        month1 = month
        year2 = year
        month2 = month
        day1 = random.choice(days)
        day2 = random.choice(days)
        while  days.index(day2) < days.index(day1)  :
            day2 = random.choice(days)
        # check if values are the same
            # then slice instead of trim
        if day1 == day2:
            day2 = None
            year2 = None
            month2 = None
        
        # pick random E
        e1 = random.choice(Es)
        e2 = random.randint(e1, 729960)
        # check if values are the same
            # then slice instead of trim
        if e1 == e2:
            e2 = None
        
        # pick random N
        n1 = random.choice(Ns)
        n2 = random.randint(n1, 5015220)
        # check if values are the same
            # then slice instead of trim
        if n1 == n2:
            n2 = None
    
        # create subsets
        subsets = S2Coverage.subset_formatter(year1, month1, day1,
                                           e1, n1, year2, month2,
                                           day2, e2, n2)
        
        return name, subsets
        # example returns 
        # name = "S2_L2A_32631_B04_10m"
        # subsets = ['ansi("2021-04-10")', 'E(719222,725355)', 'N(4997150,4999144)'] 
