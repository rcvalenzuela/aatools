
import pandas as pd

class SemanticDataFrame:
    """
    
    https://stackoverflow.com/questions/65375177/how-do-i-subclass-or-otherwise-extend-a-pandas-dataframe-without-breaking-datafr
    """
    def __init__(self, df, meta_data:dict):
        self._df = df
        self._md = meta_data
    
    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self._df, attr)
    
    def __getitem__(self, item):
        return self._df[item]
    
    def __setitem__(self, item, data):
        self._df[item] = data