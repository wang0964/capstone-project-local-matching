import tkinter as tk
from tkinter import filedialog
import os
from pathlib import Path
import glob
import pandas as pd
import MatchValue
import threading



class MainFrame(tk.Frame):
    faculty_file=''
    partner_file=''
    match_result=None
    rest_time=0
    refresh_interval=20
    second_cal=0
    last_second=0
    
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(padx=20, pady=20)
        self.create_widgets()

    def get_download_folder(self):
        if os.name == 'nt':  # Windows
            return str(Path.home() / "Downloads")
        else:  # macOS, Linux
            return os.path.join(os.path.expanduser("~"), "Downloads")
        
        
    def find_latest_csv(self,filename):

        pattern = os.path.join(self.get_download_folder(), filename)
        matched_files = glob.glob(pattern)
        
        if not matched_files:
            print("No files are found")
            return None

        latest_file = max(matched_files, key=os.path.getmtime)
        return latest_file        
        

    def create_widgets(self):
        self.select_file1_btn = tk.Button(self, text="Select faculty data file", command=self.select_file1)
        self.select_file1_btn.pack(pady=5)

        self.disable_var = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(
            self,
            text="Find Data Files Automatically",
            variable=self.disable_var,
            command=self.auto_find
        )
        self.checkbox.pack(pady=10)
        
        self.label1 = tk.Label(self, text="Project Ideas:", font=("Arial", 12))
        self.label1.pack(pady=5)        
        
        text_frame = tk.Frame(self)
        text_frame.pack(pady=10)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_output = tk.Text(text_frame, height=10, width=50, yscrollcommand=scrollbar.set)
        self.text_output.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar.config(command=self.text_output.yview)
        
        row_frame = tk.Frame(self)
        row_frame.pack(pady=10)

        self.label2 = tk.Label(row_frame, text="Top", font=("Arial", 12))
        self.label2.pack(side=tk.LEFT)

        self.N_value = tk.Text(row_frame, height=1, width=5)
        self.N_value.pack(side=tk.LEFT, padx=5)
        self.N_value.insert(tk.END, "3")

        self.label3 = tk.Label(row_frame, text="Match Results:", font=("Arial", 12))
        self.label3.pack(side=tk.LEFT)
        
        self.show_result = tk.Text(self, height=5, width=50, state='disabled')
        self.show_result.pack(pady=10)        
        
        self.match_btn = tk.Button(self, text="Match", command=self.match, width=30)
        self.match_btn.config(state="disabled")
        self.match_btn.pack(pady=15)   
        
        self.after(self.refresh_interval, self.update_match)     


    def select_file1(self):
        file_path = filedialog.askopenfilename(title="Select faculty data file", 
                                               initialdir= self.get_download_folder(),
                                               filetypes=[
                                                    ("Faculty Member List", "Faculty Member List*.csv"),
                                                    ("All csv files", "*.csv"),
                                                ]
                                               )
        if file_path:
            faculty_file=file_path
            self.match_btn.config(state="normal")

            
    def auto_find(self):
        self.faculty_file=None
        if self.disable_var.get():
            self.select_file1_btn.config(state="disabled")
            self.faculty_file=self.find_latest_csv("Faculty Member List*.csv")
            if self.faculty_file:
                self.match_btn.config(state="normal")
            else:
                self.match_btn.config(state="disabled")
                
        else:
            self.select_file1_btn.config(state="normal")
            self.match_btn.config(state="disabled")
             
    def update_result(self, content):
        self.show_result.config(state='normal')
        self.show_result.delete("1.0", tk.END)
        self.show_result.insert(tk.END, content)
        self.show_result.config(state='disabled')
    
    
    def get_top_n(self,lst,n=0):
        dictlist=[]
        if n>len(lst) or n<1:
            n=len(lst)
            
        for i in range(n):
            dictlist.append(lst[i])
            
        key_list=list(dictlist[0].keys())
        key_list.remove('score')
        id_name=key_list[0]

        result=f'{dictlist[0][id_name]}'
        for i in range(1,n):
            result += ','+f'{dictlist[i][id_name]}'
            
        return result    
    
    def match(self):
        content = self.text_output.get("1.0", tk.END).strip()
        new_match=MatchValue.Match(self.faculty_file, content)
        # result=new_match.match()
        self.match_result=None
        self.show_result.config(state='normal')
        self.show_result.delete("1.0", tk.END)
        
        threading.Thread(target=new_match.match,args=(self,)).start()
        
        # n=self.N_value.get("1.0", tk.END).strip()
        
        # try:
        #     n=int(n)
        # except:
        #     n=3
            
        # result=self.get_top_n(result,n)
        
        # self.update_result(result)
        self.after(self.refresh_interval, self.update_match)


    def update_match(self):
        if self.match_result:
            n=self.N_value.get("1.0", tk.END).strip()
            
            try:
                n=int(n)
            except:
                n=3
                
            result=self.get_top_n(self.match_result,n)          
            self.update_result(result)
            self.match_result=None
            
        # if ("Matching" in self.match_btn['text']) and (self.match_btn['state']=='disable') and (self.rest_time>0):
        #     if self.last_second != self.rest_time:
        #         second_cal=0
        #         self.last_second = self.rest_time
            
        #     self.second_cal +=self.refresh_interval
        #     if second_cal>=1000:
        #         self.rest_time -= 1
        if self.rest_time!=0:    
            self.match_btn.config(text=f"Matching    ({self.rest_time}s left)")
        
        self.after(self.refresh_interval, self.update_match)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Matching kit desktop version")
    app = MainFrame(master=root)
    app.mainloop()
