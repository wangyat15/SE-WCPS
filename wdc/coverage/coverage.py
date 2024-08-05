import numpy as np
import random
import os
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
sprint_1_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(sprint_1_directory)
class Coverage:
    '''
    Class containing coverages
    
    Information obtained from https://standards.rasdaman.com/demo_wcs.html 
    '''

    def __init__(self, coverage_name, index = None):
        self.coverage_name = coverage_name
        self.index = index

    def check_index(self, index: str):
        return index in self.index
    
    def put_slice(self, index: str, slice: str):
        f = self.check_index(index)
        if not f:
            return False
        self.index[index] = slice
        return True
    
