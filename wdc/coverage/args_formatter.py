from typing import List
from datetime import datetime
from helpers.subset import Subset

class Formatting:
    '''Class of static methods that help with formatting the arguments for the client requests'''
    
    @staticmethod
    def subsets_format(subsets: List[Subset]) -> str:
        '''
        Function to create sub_sets format

        Args: 
        list[Subset]:a list of subset

        Returns:
        Subset in str format

        '''
        
        subset_query =  f'{', '.join(str(subset.query) for subset in subsets)}'

        return subset_query


    # methods for ansi date formatting, both trimming and slicing
    @staticmethod
    def ansi_sliceformat(year:str, month:str, day:str):
        '''
        Function to create specific ansi date slice format
        
        Args:
        year (str): 4 digit number as string
        month (str): 2 digit number as string
        day (int): 2 digit number as string
        
        Returns:
        date (str): date in form e.g. "ansi(\"2021-04-09\")"
        '''
        # validate the date format 
        date_str = year + '-'+ month + '-' + day
        try:
           t_date = datetime.strptime(date_str,"%Y-%m-%d")
           date = "ansi(\"" + f"{year}-" 
           date += f"{month}-"
           date += f"{day}\")"
        except ValueError:
           date = "Invalid date format"  
        return date
    
    @staticmethod
    def ansi_trimformat(year1:str, month1:str, day1:str, year2:str, month2:str, day2:str):
        '''
        Function to create specific ansi date trim format
        
        Args:
        year1, year2 (str): 4 digit number as string
        month1, month2 (str): 2 digit number as string
        day1, day2 (int): 2 digit number as string
        
        Returns:
        date (str): date in form e.g. "ansi(\"2021-04-09\",\"2021-05-01\")"
        '''
        # validate the date format 
        try:
           date_str = year1 + '-'+ month1 + '-' + day1
           f_date = datetime.strptime(date_str,"%Y-%m-%d")
           date_str = year2 + '-'+ month2 + '-' + day2
           t_date = datetime.strptime(date_str,"%Y-%m-%d")
           date = "ansi(\"" + f"{year1}-" 
           date += f"{month1}-"
           date += f"{day1}\",\""  
           date += f"{year2}-"
           date += f"{month2}-"
           date += f"{day2}\")" 
        except ValueError:
           date = "Invalid date format"  
        return date
    
    # methods for E coordinates formatting, both trimming and slicing
    @staticmethod
    def E_sliceformat(coord:int):
        '''
        Function to create E coordinate slice
        
        Args:
        coord (int): coordinate of E
        
        Returns:
        e (str): in form e.g. "E(669960)"
        '''
        e = "E(" + f"{coord})" 
        return e
    
    @staticmethod
    def E_trimformat(lowb:int, upperb:int):
        '''
        Function to create E coordinates trim
        
        Args:
        lowb (int): lower bound of E subset
        upperb (int): upper bound of E subset
        
        Returns:
        e (str): in form e.g. "E(669960,729960)"
        '''
        e = "E(" + f"{lowb}," 
        e += f"{upperb})"
        return e




    # methods for N coordinates formatting, both trimming and slicing
    @staticmethod
    def N_sliceformat(coord:int):
        '''
        Function to create N coordinate slice
        
        Args:
        coord (int): coordinate of N
        
        Returns:
        n (str): in form e.g. "N(4990200)"
        '''
        n = "N(" + f"{coord})" 
        return n
    
    @staticmethod
    def N_trimformat(lowb:int, upperb:int):
        '''
        Function to create N coordinates trim
        
        Args:
        lowb (int): lower bound of N subset
        upperb (int): upper bound of N subset
        
        Returns:
        n (str): in form e.g. "N(4990200,5015220)"
        '''
        n = "N(" + f"{lowb}," 
        n += f"{upperb})"
        return n
    


    # methods for latitude formatting, both trimming and slicing
    @staticmethod
    def Lat_sliceformat(coord:int):
        '''
        Function to create Lat coordinate slice
        
        Args:
        coord (int): coordinate of latitude
        
        Returns:
        Lat (str): in form e.g. "Lat(60)"
        '''
        # Validate latitude value
        if (-90 <= coord <= 90):
           Lat = "Lat(" + f"{coord})" 
        else:
           Lat = "Invalid latitude value"
        return Lat
    
    @staticmethod
    def Lat_trimformat(lowb:int, upperb:int):
        '''
        Function to create Lat coordinates trim
        
        Args:
        lowb (int): lower bound of Lat subset
        upperb (int): upper bound of Lat subset
        
        Returns:
        Lat (str): in form e.g. "Lat(60,80)"
        '''
        # validate lower and upper latitude values
        if (-90 <= lowb <= 90) and (-90 <= upperb <= 90):
           Lat = "Lat(" + f"{lowb}," 
           Lat += f"{upperb})" 
        else:
           Lat = "Invalid latitude value"
        return Lat
    

    # methods for longitude formatting, both trimming and slicing
    @staticmethod
    def Lon_sliceformat(coord:int):
        '''
        Function to create Lon coordinate slice
        
        Args:
        coord (int): coordinate of longitude
        
        Returns:
        Lat (str): in form e.g. "Lon(60)"
        '''
        # Validate longitude value
        if (-180 <= coord <= 180):
           Lon = "Lon(" + f"{coord})" 
        else:
           Lon = "Invalid longitude value"
        return Lon
    
    @staticmethod
    def Lon_trimformat(lowb:int, upperb:int):
        '''
        Function to create Lon coordinates trim
        
        Args:
        lowb (int): lower bound of Lon subset
        upperb (int): upper bound of Lon subset
        
        Returns:
        Lon (str): in form e.g. "Lon(60,80)"
        '''
        # validate lower and upper longitude values
        if (-180 <= lowb <= 180) and (-180 <= upperb <= 180):
           Lon = "Lon(" + f"{lowb}," 
           Lon += f"{upperb})" 
        else:
           Lon = "Invalid longitude value"
        return Lon

