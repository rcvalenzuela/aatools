
import re


def create_qmd_header(title:str  # Title of the document
                     )->str:     # yaml header qmd file
    
    header = f'''---
                 title: "{title}"
                 format:
                     html:
                         code-fold: true
                 jupyter: python3
                 ---'''
    
    # Improve formatting of the string. 
    # We remove 17 empty spaces because
    header = re.sub(r"^\s{17}", "", header, 0, re.MULTILINE)

    return header


def eda_report(file_name:str,    # Name of the file to be written
               abt:SemanticDataframe          # Analytics based table on which to base the report
               )-> None:
    # Creates qmd file that when rendered generates EDA report

    with open(file_name, 'w') as f:
        # Add yaml header
        f.write(create_qmd_header('EDA Report'))