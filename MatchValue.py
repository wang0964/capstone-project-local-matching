import etl
import re
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd


model_path = r"E:\models\bart-large-mnli"
# model_path = r"E:\local_mdeberta_xnli"
# model_path = r"E:\local_DeBERTa"
# model_path = r"E:\DeBERTa-v3-fever-anli"

class Match:
    def __init__(self,faculty_file, idea):
        self.faculty_file=faculty_file
        self.idea=idea
        
        print(self.faculty_file)
        print(self.idea)
        
        
        new_etl=etl.ETL(self.faculty_file)
        
        self.faculty_df=new_etl.get_etl()
    
    
    def match(self): 
        faculty_df=self.faculty_df
        
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)

        classifier = pipeline("zero-shot-classification", 
                            model=model, 
                            tokenizer=tokenizer, 
                            framework="pt")


        project_idea=self.idea
        scores=[]
        for j, frow in faculty_df.iterrows():
            str1=frow['AcademicProgram']
            str1=re.sub(r'\(.*\)','',str1)
            str1=str1.strip()
            str2=frow['CourseName']

            s=f'{str2} for {str1}' if str2!='' else str1
            result = classifier(
                        project_idea, 
                        [str1],
                        hypothesis_template="The following text is related to {}.",
                        multi_label=True
            )
            scores.append( {'fID':frow['fID'],'score':result['scores'][0] })
        
        sorted_data = sorted(scores, key=lambda x: x['score'], reverse=True)
        
        return sorted_data
    

        