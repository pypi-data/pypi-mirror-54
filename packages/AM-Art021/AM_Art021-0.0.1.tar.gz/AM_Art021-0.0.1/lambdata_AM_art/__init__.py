
"""
lambdata_AM_Art - A Collection of Data Science helper functions.
version = 0.0.1
"""
__version__ = "0.0.1"

import pandas as pd 
import numpy as np 


def list_to_col(df1, col_name, lst): 
    """
    Takes a list, column name, and df, converts the list to a pandas series
    and adds it to the df under the column name provided.
    
    df1: pandas DataFrame
    col_name: string
    lst: list
    
    return: new DataFrame with
    """
    df2 = pd.Series(lst, name=col_name).to_frame()
    df = pd.concat([df1, df2], axis=1)
    
    return df 

def split_dates(df, col_name):
    """
    Takes a df and column name that is in MM/DD/YYYY format
    and splits it into a month, day and year column.
    
    df: pandas DataFrame
    col_name: string, column name to be split
    
    return: DateFrame with new month, day, and year columns
    """
    
    df = df.copy()
    df[col_name] =  pd.to_datetime(df[col_name], infer_datetime_format=True)
    df['month'] = df[col_name].dt.month
    df['day'] = df[col_name].dt.day
    df['year'] = df[col_name].dt.year
    
    df.drop(columns=[col_name], inplace=True)
    
    return df
