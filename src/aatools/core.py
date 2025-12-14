
import copy
import pandas as pd

class SemanticDataFrame:
    """
    
    Notes
    -----

    The class follows the method proposed in:
        https://stackoverflow.com/questions/65375177/how-do-i-subclass-or-otherwise-extend-a-pandas-dataframe-without-breaking-datafr
    
    The meta_data dict has as keys the columns of interest of the data frame

    We distinguish four types of variables:
    - binary
    - nominal
    - ordinal
    - ratio

    The structure of the dict shall be as follows:
    meta_data:
        var_name_1:
          vis_name: Name to display in visualizations
          table_name: Name to display in tables
          type: binary | nominal | ordinal | ratio
        var_name_2:
          ...
    """
    def __init__(self, df, meta_data:dict):
        """
        Notes
        -----
        The structure of the dict shall be as follows:
        md:
          vars:
            var_name_1:
            vis_name: Name to display in visualizations
            table_name: Name to display in tables
            type: binary | nominal | ordinal | ratio
            var_name_2:
            ...
          ratio_vars:
          ordinal_vars:
          nominal_vars:
          binary_vars:

        """
        # Set values
        self._df = df
        # Initialize metadata
        md = dict()
        md['vars'] = copy.deepcopy(meta_data)
        
        # Generate list
        # Must check that variables have the correct type

        self._md = meta_data
    
    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self._df, attr)
    
    def __getitem__(self, item):
        return self._df[item]
    
    def __setitem__(self, item, data):
        self._df[item] = data
    
    def vis_name(self, var_name:str) -> str:
        """Visualization name of var_name
        
        Parameters
        ----------
        var_name
            Column name of the variable
        
        """
        return self._md['vars'][var_name]['vis_name']
    
    def ratio_vars(self) -> list:
        """List of ratio variables in data"""
        return self._df['ratio_vars']
    
    def ordinal_vars(self) -> list:
        """List of ordinal variables in data"""
        return self._df['ordinal_vars']
    
    def nominal_vars(self) -> list:
        """List of nominal variables in data"""
        return self._df['nominal_vars']
    
    def binary_vars(self) -> list:
        """List of binary variables in data"""
        return self._df['binary_vars']