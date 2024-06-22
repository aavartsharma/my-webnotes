import os
import json
import pandas as pd
import time
import tkinter as tk
import random 
from tkinter import messagebox

json_file_path = "data.json"

def givename():
    return "gtya"+ random.choice(list("abcdefghijklmnopqrstuvwxyz"))

def read_the_json():
    with open(json_file_path, 'r') as file:
        json_var = json.load(file)
    return json_var
       
def write_the_json(data={}):
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

class file_info:
    def __init__(self,fileName,color):
        self.file_name = str(fileName)
        self.file_number_base64 = givename()
        self.file_color = color
        self.chapter_dict = {}

    def changeFilename(self,name):
        self.file_name = str(name)
    
    def AddChapter(self,name):  # chapter
        self.chapter_dict[name] = {}
         
    def AddSubChapter(self,name,title):
        self.chapter_dict[name][title] = []
       
    def AddLinesToSubchapter(self,name,title,line):
        self.chapter_dict[name][title].append(line) 
    
    def AddLinesToSubchaptertoline(self,name,title,line,linenumber):
        self.chapter_dict[name][title][linenumber] = line
    def __str__(self):
        print(self.chapter_dict)
        return f"file(name={self.file_name},filenameinbase64 = {self.file_number_base64}, filecolor={self.file_color})"
    

try:
    json_Dict = read_the_json()
    print(type(json_Dict))
except:
    write_the_json({})

print(givename())

root = tk.Tk()
root.title("webNotes")
# file_name = ""
def display_UI(): # for diplaying message
    user_text = text_area.get("1.0",tk.END)
    global file_name
    file_name = user_text
    messagebox.showinfo("Entered Text",user_text.strip())
#root.attributes("-fullscreen", True)
text_area = tk.Text(root,height=1,width=40)
text_area.pack(pady=10)

submit_button = tk.Button(root,text="Submit",command=display_UI)
submit_button.pack(pady=10)

dropdown_var = tk.StringVar(root)
dropdown_var.set("Option 1")  # Default value
options = ["Option 1", "Option 2", "Option 3", "Option 4"]
dropdown_menu = tk.OptionMenu(root, dropdown_var, *options)
dropdown_menu.pack(pady=50) 
root.mainloop()

# os.makedirs(file_name,exist_ok=True) # file name is not defined

html_code = ""
exit()
html_file_path = os.path.join(file_name,'index.html')

with open(html_file_path,'w') as html_file:
    html_file.write(html_code)

print("webnote was made sucessfully")