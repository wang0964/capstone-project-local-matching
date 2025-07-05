import etl
import re
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import time


model_path = r"E:\models\bart-large-mnli"
# model_path = r"E:\local_mdeberta_xnli"
# model_path = r"E:\local_DeBERTa"
# model_path = r"E:\DeBERTa-v3-fever-anli"

class Match:
    def __init__(self,selected_file, txt, option):
        self.selected_file=selected_file
        self.input_txt=txt
        
        print(self.selected_file)
        print(self.input_txt)
        self.option=option
        
        new_etl=etl.ETL(self.selected_file, option)
        
        self.df=new_etl.get_etl()
   

    def match(self,parent): 
        total_row = len(self.df)
        if total_row==0:
            return None
        
        start_time=time.time()

        
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        
        parent.match_btn.config(text="Matching")
        parent.match_btn.config(state="disabled")
        select_btn_state=parent.select_file1_btn['state']
        parent.select_file1_btn.config(state='disabled')
        checkbox_state=parent.checkbox['state']
        parent.checkbox.config(state='disabled')
        parent.radio1.config(state="disabled")
        parent.radio2.config(state="disabled")

        classifier = pipeline("zero-shot-classification", 
                            model=model, 
                            tokenizer=tokenizer, 
                            framework="pt")

        scores=[]
        current_row=0
        
        for j, row in self.df.iterrows():
            current_row += 1
            if self.option==1:
                str0=self.input_txt
                str1=row['AcademicProgram']
                str1=re.sub(r'\(.*\)','',str1)
                str1=str1.strip()
                id='fID'                
            else:
                str0=row['ProjectIdea']
                str1=self.input_txt
                id='pID'

            result = classifier(
                        str0, 
                        [[str1]],
                        hypothesis_template="The course is related to {}.",
                        multi_label=True
            )
            scores.append( {id:row[id],'score':result['scores'][0] })
        
            using_time = time.time() -start_time
            parent.rest_time= int((using_time / current_row) * (total_row- current_row))
            
        
        sorted_data = sorted(scores, key=lambda x: x['score'], reverse=True)
        
        parent.match_btn.config(text="Match")
        parent.match_btn.config(state="normal")
        parent.rest_time=0

        parent.select_file1_btn.config(state=select_btn_state)
        parent.checkbox.config(state=checkbox_state)      
        parent.radio1.config(state="normal")
        parent.radio2.config(state="normal")  
        
        parent.match_result=sorted_data
        
        return sorted_data        