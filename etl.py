import os
from pathlib import Path
import pandas as pd

class ETL:
    
    def __init__(self,faculty_file):
        self.faculty_file=faculty_file
        print(self.faculty_file)
        
        
    def extract(self):
        self.faculty_df=pd.read_csv(self.faculty_file)
    
    def transform(self):
        self.faculty_df=self.faculty_df[(self.faculty_df['Approved']=='Yes') & (self.faculty_df['Matched']=='No')]
        self.faculty_df = self.faculty_df[['ID', 'AcademicProgram', 'CourseName']]
        
        self.faculty_df = self.faculty_df.rename(columns={'ID': 'fID'})

        self.faculty_df['fID']=self.faculty_df['fID'].astype(int)
        self.faculty_df['pmatch']=''
        
    def get_etl(self):
        self.extract()
        self.transform()
        return self.faculty_df