import os
import json
import pandas as pd
import time
import tkinter as tk
import random 
from tkinter import messagebox
from tkinter import ttk
from tkinter import colorchooser
from tkinter import font

verision = "1.0.1"
json_file_path = "data.json"
sample = { "File Name":[f"file_{i}" for i in range(10)],
          'Sheet Name': [f"sheet_{i}" for i in range(10)],
          'Number Of Rows': [f"row_{i}" for i in range(10)],
          'Number Of Columns': [f"col_{i}" for i in range(10)]
         }

def base10_to_base64(num):
    if num == 0:
        return 'A'
    
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    base64_string = ""
    
    while num > 0:
        remainder = num % 64
        base64_string = base64_chars[remainder] + base64_string
        num = num // 64
    
    return base64_string

def givename():
    current_time= time.localtime()

    day = current_time.tm_mday
    month = current_time.tm_mon
    year = current_time.tm_year
    firstpart = base10_to_base64(day)+base10_to_base64(month)+base10_to_base64(year)
    secondpart = str(len(sample)+1)
    return firstpart + secondpart
print(givename())
def read_the_json():
    with open(json_file_path, 'r') as file:
        json_var = json.load(file)
    return json_var
       
def write_the_json(data={}):
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

class file_info:
    def __init__(self,fileName,color,textColor,version):
        self.file_name = str(fileName)
        self.file_number_base64 = givename()
        self.file_color = color
        self.text_color = textColor
        self.version = version
        self.chapter_dict = {}

    def changeFilename(self,name):
        self.file_name = str(name)

    def changeFileBackGround(self,newcolor):
        self.file_color = newcolor
    
    def changeTextColor(self,newcolor):
        self.text_color = newcolor
    def changeversion(self,newverision):
        self.version = newverision

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
except:
    write_the_json({})


def display_UI(content): # for diplaying message
    user_text = content.get("1.0",tk.END)
    print(user_text)
    global file_name
    file_name = user_text
    # messagebox.showinfo("Entered Text","the file was made do you want to open")  # user_text.strip()
    if messagebox.askyesno("Open", "The file was made successfully. Do you want to open the notesite?"):
        pass  # open the file 

def close_window(root):
    if messagebox.askyesno("Close", "Are you sure you want to close the window?"):
        root.destroy()

def choose_color(colorselect):
    color_code = colorchooser.askcolor(title="Choose a color")
    if color_code:
        print(f"Selected color: {color_code[1]}")
        print(color_code)
        colorselect.config(text= '             ')
        colorselect.config(background = f"{color_code[1]}")

def h():
    print("added the line")

def show_welcome_page():
    root = tk.Tk()
    root.title("webnotes")
    root.config(background="black")
    main_frame = ttk.Frame(root, padding="10", borderwidth=2, relief="solid")
    main_frame.pack(fill='both', expand=True)
    custom_font = font.Font(family="Helvetica", size=25, weight="bold")
    ttk.Label(main_frame,text="Welcome to notesite",font=custom_font).grid(row=0,column=2,padx=10,pady=5)
    # exit button ,new ,search ,edit
    button_frame = ttk.Frame(root,padding=(20,5),borderwidth=2, relief="solid")
    # button_frame.grid(row=0, column=0, sticky="nsew")
    button_frame.pack(fill='both', expand=True)
    ttk.Button(button_frame, text= "make new note",command= show_UI_new_Project).grid(row=1,column=1,padx=10,pady=5)
    ttk.Button(button_frame,text="change contant",command=None).grid(row=1,column=2,padx=20,pady=5)
    ttk.Button(button_frame,text="show all notesites",command=show_all_notesites).grid(row=2,column=1,padx=20,pady=5)
    ttk.Button(button_frame, text="Quit", command=lambda: close_window(root)).grid(row=2, column=2, padx=10, pady=5)
    root.mainloop()

def show_all_notesites():
    root = tk.Tk()
    root.title("all notes")
    for i in range(3):
        df = pd.DataFrame(sample)
        df.index = pd.Index(range(1, len(df) + 1))
        print(df)
        cols = list(df.columns)

        tree = ttk.Treeview(root)
        tree.pack()
        tree["columns"] = cols
        for i in cols:
            tree.column(i, anchor="w")
            tree.heading(i, text=i, anchor='w')

        for index, row in df.iterrows():
            tree.insert("",tk.END,text=index,values=list(row))
        print(df)
    
    root.mainloop()

def change_contant_of_notesites():
    root = tk.Tk()
    root.title("change contant")
    root.mainloop()

def show_UI_new_Project():
    root = tk.Tk()
    root.title("Make New note")
    root.config(background="lightblue")
    label = ttk.Label(root, text="Enter name of project:")
    label.grid(row=0, column=0, padx=10, pady=5)
    text_area = ttk.Entry(root,width=40)
    text_area.grid(row=0, column=1, padx=10, pady=5)

    DDlabel = ttk.Label(root,text = "choose the type:")
    DDlabel.grid(row=1,column=0,padx=10,pady = 5)
    text_area = ttk.Entry(root,width=40)
    dropdown_var = tk.StringVar(root)
    dropdown_var.set("None")  # Default value
    options = ["Choose Type"] + ["Option 1", "Option 2", "Option 3","Option 4"]+["None"]
    dropdown_menu = ttk.OptionMenu(root, dropdown_var, *options)
    dropdown_menu.grid(row=1, column=1, padx=10, pady=5) #pady = 50

    colorselect1 = ttk.Label(root, text= "None")
    colorlabel = ttk.Label(root, text="choose the text color:")
    colorlabel.grid(row=2,column=0,padx=10,pady=5)
    colorbutton = ttk.Button(root, text="Choose Color", command= lambda: choose_color(colorselect1))
    colorbutton.grid(row=2,column=1,padx=10,pady=5)
    colorselect1.grid(row=2,column=2,padx=15,pady=5)

    colorselect2 = ttk.Label(root, text= "None")
    colorlabel = ttk.Label(root, text="choose the backGround color:")
    colorlabel.grid(row=3,column=0,padx=10,pady=5)
    colorbutton = ttk.Button(root, text="Choose Color", command= lambda: choose_color(colorselect2))
    colorbutton.grid(row=3,column=1,padx=10,pady=5)
    colorselect2.grid(row=3,column=2,padx=15,pady=5)

    label = ttk.Label(root, text="Enter Chapter Name:")
    label.grid(row=4, column=0, padx=10, pady=5)
    entry = ttk.Entry(root,width=40)
    entry.grid(row=4, column=1, padx=10, pady=5)

    label = ttk.Label(root, text="Enter Sub-Chapter Name:")
    label.grid(row=5, column=0, padx=10, pady=5)
    entry = ttk.Entry(root,width=40)
    entry.grid(row=5, column=1, padx=10, pady=5)

    label = ttk.Label(root, text = "Enter the content:")
    label.grid(row=6,column=0,padx=10,pady=5)
    content = tk.Text(root,width=50,height=10)
    default_text = "Add your note here."
    content.insert("1.0", default_text)
    content.grid(row=6,column=1,padx=10,pady=5)

    addLineButton = ttk.Button(root,text="Add",command=h)
    addLineButton.grid(row=8,column=1,padx=10,pady=5)

    submit_button = ttk.Button(root,text="make new note",command=lambda: display_UI(content))
    submit_button.grid(row=9, column=1, padx=10, pady=5)

    close_button = ttk.Button(root, text="Quit", command=lambda: close_window(root))
    close_button.grid(row=9, column=2, padx=10, pady=5)

    root.mainloop()

show_UI_new_Project()
# show_welcome_page()
# os.makedirs(file_name,exist_ok=True) # file name is not defined

html_code = ""
exit()

html_file_path = os.path.join(file_name,'index.html')

with open(html_file_path,'w') as html_file:
    html_file.write(html_code)

print("webnote was made sucessfully")