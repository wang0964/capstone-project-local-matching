import os
from pathlib import Path
import pandas as pd

class ETL:
    
    def __init__(self,selected_file,option):
        self.selected_file=selected_file
        self.option=option
        print(self.selected_file)
        print(self.option)
        
        
    def extract(self):
        self.df=pd.read_csv(self.selected_file)
    
    def transform(self):
        if self.option==1:
            self.df=self.df[(self.df['Approved']=='Yes') & (self.df['Matched']=='No')]
            self.df = self.df[['ID', 'AcademicProgram', 'CourseName']]
            
            self.df = self.df.rename(columns={'ID': 'fID'})

            self.df['fID']=self.df['fID'].astype(int)
            self.df['pmatch']=''
        else:
            self.df=self.df[(self.df['Approved']=='Yes') & (self.df['Matched']=='No')]
            self.df = self.df[['ID','ProjectIdea']]
            
            self.df = self.df.rename(columns={'ID': 'pID'})

            self.df['pID']=self.df['pID'].astype(int)
            self.df['fmatch']=''    
            
                
    def get_etl(self):
        self.extract()
        self.transform()

        return self.df