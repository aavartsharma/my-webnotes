import os
import json
import time
import shutil
import platform
import pandas as pd
import tkinter as tk
import webbrowser as wb
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from tkinter import colorchooser

current_verision = "1.0.1"
json_file_path = "data.json"
file_directory_path = 'my notes'
welcome_root = None
demo_root = None

sample = {"File Name":[f"file_{i+1}" for i in range(10)],
          'Sheet Name': [f"sheet_{i+1}" for i in range(10)],
          'Number Of Rows': [f"row_{i+1}" for i in range(10)], 
          'Number Of Columns': [f"col_{i+1}" for i in range(10)]
}

text_color_hexcode = ""
background_color_hexcode = ""
notesiteTag = ["code","img","link"]

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

def check_platform():
    os_platform = platform.system()
    if os_platform == "Linux":
        # Check for Android-specific details if on Linux
        if "ANDROID_ARGUMENT" in os.environ:
            return "Android"
        else:
            return "Linux"
    elif os_platform == "Windows":
        return "Windows"
    elif os_platform == "Darwin":
        return "PC macOS"
    else:
        return "Unknown platform"

def givename():
    info_dict = read_the_json()
    current_time= time.localtime()
    day = current_time.tm_mday
    month = current_time.tm_mon
    year = current_time.tm_year
    firstpart = base10_to_base64(day) + base10_to_base64(month) + base10_to_base64(year)
    projects = 0
    for i in info_dict:
        projects += len(info_dict[i]) + 1
    secondpart = str(projects)
    return firstpart + secondpart

def read_the_json():
    with open(json_file_path, 'r') as file:
        json_var = json.load(file)
    return json_var
       
def write_the_json(data={}):
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

class file_info:
    def __init__(self,fileName,version):
        self.file_name = str(fileName)
        self.file_number_base64 = givename()
        self.version = version
        self.color_dict = {}
        self.chapter_dict = {}

    def changeFilename(self,name):
        self.file_name = str(name)

    def changeColorDict(self,dict):
        self.color_dict = dict
    
    def changeColor(self,color,colorNameInHex):
        self.color_dict[color] = colorNameInHex
    
    def changeversion(self,newcurrent_verision):
        self.version = newcurrent_verision
    
    def AddDictDrictly(self, dict):
        self.chapter_dict = dict

    def AddChapter(self,name):  # chapter
        self.chapter_dict[name] = {}
         
    def AddSubChapter(self,name,title):
        self.chapter_dict[name][title] = []
       
    def AddLinesToSubchapter(self,name,title,line):
        self.chapter_dict[name][title].append(line) 
    
    def AddLinesToSubchaptertoline(self,name,title,line,linenumber):
        self.chapter_dict[name][title][linenumber] = line
    
    def __str__(self):
        return f"file(name={self.file_name},filenameinbase64 = {self.file_number_base64},verision = {self.version}, filecolor={self.color_dict},chapter_dict={self.chapter_dict})"

def make_class_dict(note_class_object):
    return {note_class_object.file_name : {
        "number": str(note_class_object.file_number_base64),
        "webnote_version" : str(current_verision),
        "colors" : note_class_object.color_dict,
        "content" : note_class_object.chapter_dict
    }}


try:
    json_Dict = read_the_json()
except:
    write_the_json({})

def saveObject(type_of_file,name,color_dict = {}, dict ={}):
    fileObject = file_info(name,current_verision)
    fileObject.changeColorDict(color_dict)
    fileObject.AddDictDrictly(dict)
    json_file_data = read_the_json()
    try:
        json_file_data[type_of_file].update(make_class_dict(fileObject))
    except:
        json_file_data[type_of_file] = {}
        json_file_data[type_of_file].update(make_class_dict(fileObject))
        
    write_the_json(json_file_data)

def make_all_line_in_note(text): # make dict
    manlist = []
    alllines = text.split("\n")
    for i in range(len(alllines)):
        alllines[i] = alllines[i].rstrip()
    indexingNUmber = 0
    for i in alllines:
        a = i.replace("?","").replace("|","").strip()
        if a in notesiteTag:
            lineplace = alllines.index(f"|{a}?")
            lineEnd = alllines.index(f"|/{a}?")
            #print(alllines[lineplace:(lineEnd+1)])
            print(f"a={i} , line = {lineplace}")
            manlist.append({"type" : a,"text" : alllines[lineplace:(lineEnd+1)],"place":lineplace-1+indexingNUmber})
            indexingNUmber += 1
            for i in alllines[lineplace:(lineEnd+1)]:
                del alllines[alllines.index(i)]
    for i in alllines:  # if normal text
        # manlist.replace(i,{"type": "text","text": i}) # replace
        alllines[alllines.index(i)] = {"type": "text","text": i}
    
    linofdict = 0
    for i in manlist:
        alllines.insert(i["place"] + 1,manlist[linofdict])
        linofdict += 1
     
    return alllines

def make_html_file(filename,filenumber,dict_of_chapter = {},colordict = {}):
    #html_content = ""
    # Create the directory if it doesn't exist
    if not os.path.exists(file_directory_path):
        os.mkdir(file_directory_path)

    # Define the HTML content
    with open("index.html") as file:
        html_content = file.read()
        html_content = html_content.replace('"MainDict/**/"',str(dict_of_chapter))
        html_content = html_content.replace("TextColor/**/",str(colordict["text-color"]))
        html_content = html_content.replace("Background_Color/**/",str(colordict["background-color"]))
        html_content = html_content.replace("ProjectName/**/",filename)
        html_content = html_content.replace("ProjectFileNumber/**/",filenumber)
    
    # Define the file path
    file_path = os.path.join(file_directory_path, filename)
    os.makedirs(file_path, exist_ok=True)
    html_file = os.path.join(file_path,"index.html")
    pictureFile = os.path.join(file_path,"pics")                                         # left here
    # for text_dict in dict_of_chapter:
    #     if(text_dict["type"] == "img"):
    #         for lines in text_dict["text"]:
    #             if("path=" in lines):
    #                 lines.replace("path=","")
    #                 os.makedirs(os.path.dirname(lines), exist_ok=True)
    #                 shutil.copy(lines, destination)
    # Write HTML content to the new file
    try:
        with open(html_file, 'w') as file:
            file.write(html_content)
    except:
        print("something went wrong.")
    return html_file


def make_note_button(content,type_of_file,name,filenumber, dict ={},colordict = {}): # for diplaying message
    user_text = content.get("1.0",tk.END)
    typeofNote = ""
    if(type_of_file[0] == ""):
        typeofNote = type_of_file[1]
    else:
        typeofNote = type_of_file[0]
    saveObject(typeofNote,name,colordict,dict)
    file_path_html_created = make_html_file(name,filenumber,dict,colordict)
    if messagebox.askyesno("Open", "The file was made successfully.\n Do you want to open the notesite?"):
        wb.open(file_path_html_created) 
    else:
        pass

def close_window(root):
    if messagebox.askyesno("Close", "Are you sure you want \nto close the window?"):
        root.destroy()

def choose_color1(colorselect,color_dict = {}):
    color_code = colorchooser.askcolor(title = "Choose a color")
    if (None not in color_code):
        colorselect.config(text= '             ')
        colorselect.config(background = f"{color_code[1]}")
        color_dict["text-color"] = str(color_code[1])
        return str(color_code)

def choose_color2(colorselect,color_dict = {}):
    color_code = colorchooser.askcolor(title = "Choose a color")
    if (None not in color_code):
        colorselect.config(text= '             ')
        colorselect.config(background = f"{color_code[1]}")
        color_dict["background-color"] = str(color_code[1])
        return str(color_code)



def add_Line_Button(chapter,sub_chapter,text,dict):
    chapter_name = chapter.get()
    sub_chapter_name = sub_chapter.get()
    content_text = text.get("1.0",tk.END)
    list_of_notes = make_all_line_in_note(content_text)
    try:
        dict[chapter_name].update({sub_chapter_name:list_of_notes})
    except:
        dict[chapter_name] = {}
        dict[chapter_name].update({sub_chapter_name:list_of_notes})

    global demo_root
    if demo_root is None:  # Check if root is None, meaning it hasn't been created yet
        demo_root = tk.Tk()
        demo_root.title("Demo")
        custom_font = font.Font(family="Helvetica", size=25, weight="bold")
        bold_font = ("Helvetica", 24, "bold")
        bold_font_h2 = ("Helvetica", 16, "bold")
        print(dict)
        for chapter in dict:
            ttk.Label(demo_root, text=("" + chapter+ "     "), font=bold_font).pack(fill="x")
            for sub_chapter in dict[chapter]:
                ttk.Label(demo_root, text=("         " + sub_chapter+ "     "), font=bold_font_h2).pack(fill="x")
                for line_dict in dict[chapter][sub_chapter]:
                    print(line_dict)
                    if(line_dict["type"] == "text"):
                        ttk.Label(demo_root, text=(" "*20 + line_dict["text"] + "     "), font=custom_font).pack(fill="x")
                    
                        
        demo_root.mainloop()
    else:
        for widget in demo_root.winfo_children():
            widget.destroy() 
        custom_font = font.Font(family="Helvetica", size=25, weight="bold")
        bold_font = ("Helvetica", 24, "bold")
        bold_font_h2 = ("Helvetica", 16, "bold")
        for chapter in dict:
            ttk.Label(demo_root, text=("" + chapter+ "     "), font=bold_font).pack(fill="x")
            for sub_chapter in dict[chapter]:
                ttk.Label(demo_root, text=("         " + sub_chapter+ "     "), font=bold_font_h2).pack(fill="x")
                for line_dict in dict[chapter][sub_chapter]:
                    if(line_dict["type"] == "text"):
                        ttk.Label(demo_root, text=(" "*20 + line_dict["text"] + "     "), font=custom_font).pack(fill="x")
                        
                    
        # ttk.Label(demo_root,text=dict,font=custom_font).pack()
        demo_root.config(background="black")
        demo_root.mainloop()  

def show_welcome_page():
    root = tk.Tk()
    root.title("webnotes")
    root.config(background="black")
    main_frame = ttk.Frame(root, padding="10", borderwidth=2, relief="solid")
    main_frame.pack(fill='both', expand=False)
    custom_font = font.Font(family="Helvetica", size=25, weight="bold")
    ttk.Label(main_frame,text="Welcome to notesite",font=custom_font).grid(row=0,column=2,padx=10,pady=5)
    # exit button ,new ,search ,edit
    button_frame = ttk.Frame(root,padding=(20,5),borderwidth=2, relief="solid")
    # button_frame.grid(row=0, column=0, sticky="nsew")
    button_frame.pack(fill='both', expand=True)
    ttk.Button(button_frame, text= "make new note",command= show_UI_new_Project).grid(row=1,column=1,padx=10,pady=5)
    ttk.Button(button_frame, text="delete a note",command=delete_notesites).grid(row=1,column=2,padx=20,pady=5)
    ttk.Button(button_frame, text="show all notesites",command=show_all_notesites).grid(row=2,column=1,padx=20,pady=5)
    ttk.Button(button_frame, text="Quit", command=lambda: close_window(root)).grid(row=2, column=2, padx=10, pady=5)
    root.mainloop()
    
    
def show_welcome_android_page():
    root = tk.Tk()
    root.title("webnotes")
    root.config(background="black")

    main_frame = ttk.Frame(root, padding="10", borderwidth=2, relief="solid")
    main_frame.pack(fill='both', expand=False)
    custom_font = font.Font(family="Helvetica", size=20, weight="bold")
    ttk.Label(main_frame,text="Welcome to notesite",font=custom_font).grid(row=0,column=0,padx=0,pady=5)
    # exit button ,new ,search ,edit
    button_frame = ttk.Frame(root,padding=(20,5),borderwidth=2, relief="solid")
    # button_frame.grid(row=0, column=0, sticky="nsew")
    button_frame.pack(fill='both', expand=True)
    ttk.Button(button_frame, text= "make new note",command= show_UI_new_Project).grid(row=1,column=0,padx=20,pady=5)
    ttk.Button(button_frame,text="delete a note",command=delete_notesites).grid(row=1,column=1,padx=20,pady=5)
    ttk.Button(button_frame,text="show all notesites",command=show_all_notesites).grid(row=2,column=0,padx=20,pady=5)
    ttk.Button(button_frame, text="Quit", command=lambda: close_window(root)).grid(row=2, column=1, padx=20, pady=5)
    root.mainloop()

def make_dataFrame_dict(dict):
    new_dict = {}
    name = []
    number = []
    verision = []
    for i in dict:
        name.append(i)
        number.append(dict[i]["number"])
        verision.append(dict[i]["webnote_version"])
    new_dict["File Name"] = name
    new_dict["File Number"] = number
    new_dict["verision"] = verision
    return new_dict

def show_all_notesites():
    root = tk.Tk()
    root.title("all notes")
    projects_dict = read_the_json()
    for i in projects_dict:
        ttk.Label(root, text=i).pack()
        df = pd.DataFrame(make_dataFrame_dict(projects_dict[i]))
        df.index = pd.Index(range(1, len(df) + 1))
        cols = list(df.columns)

        tree = ttk.Treeview(root)
        tree.pack(padx=20,pady=5)
        tree["columns"] = cols
        for i in cols:
            tree.column(i, anchor="w")
            tree.heading(i, text=i, anchor='w')

        for index, row in df.iterrows():
            tree.insert("",tk.END,text=index,values=list(row))
    
    root.mainloop()

def delete_notesites():
    root = tk.Tk()
    root.title("delete file")
    ttk.Label(root,text= "who am I?").pack()
    root.mainloop()

def show_UI_new_Project():
    root = tk.Tk()
    root.title("Make New note")
    root.config(background="lightblue")
    label = ttk.Label(root, text="Enter name of project:")
    label.grid(row=0, column=0, padx=10, pady=5)
    projectNameInput = ttk.Entry(root,width=70)
    projectNameInput.grid(row=0, column=1, padx=10, pady=5,columnspan=2)
    
    color_dictory = {}  # will contain color info
    note_dict = {}  # will contains chapter info

    DDlabel = ttk.Label(root,text = "choose the type:")
    DDlabel.grid(row=1,column=0,padx=10,pady = 5)
    type_text_area = ttk.Entry(root,width=40)   # not added to the scene
    type_text_area.grid(row=1,column=2)
    dropdown_var = tk.StringVar(root)
    dropdown_var.set("None")  # Default value
    json_file_contant = read_the_json()
    options = ["Choose Type"] + [*json_file_contant] + ["None"]
    
    dropdown_menu = ttk.OptionMenu(root, dropdown_var, *options)
    dropdown_menu.grid(row=1, column=1, padx=10, pady=5) #pady = 50

    colorselect1 = ttk.Label(root, text= "None")
    colorlabel = ttk.Label(root, text="choose the text color:")
    colorlabel.grid(row=2,column=0,padx=10,pady=5)
    colorbutton = ttk.Button(root, text="Choose Color", command= lambda: choose_color1(colorselect1,color_dictory))
    colorbutton.grid(row=2,column=1,padx=10,pady=5)
    colorselect1.grid(row=2,column=2,padx=15,pady=5)

    colorselect2 = ttk.Label(root, text= "None")
    colorlabel = ttk.Label(root, text="choose the backGround color:")
    colorlabel.grid(row=3,column=0,padx=10,pady=5)
    colorbutton = ttk.Button(root, text="Choose Color", command= lambda: choose_color2(colorselect2,color_dictory))
    colorbutton.grid(row=3,column=1,padx=10,pady=5)
    colorselect2.grid(row=3,column=2,padx=15,pady=5)

    label = ttk.Label(root, text="Enter Chapter Name:")
    label.grid(row=4, column=0, padx=10, pady=5)
    chapter_entry = ttk.Entry(root,width=70)
    chapter_entry.grid(row=4, column=1, padx=10, pady=5,columnspan=2)

    label = ttk.Label(root, text="Enter Sub-Chapter Name:")
    label.grid(row=5, column=0, padx=10, pady=5)
    sub_entry = ttk.Entry(root,width=70)
    sub_entry.grid(row=5, column=1, padx=10, pady=5,columnspan=2)

    label = ttk.Label(root, text = "Enter the content:")
    label.grid(row=6,column=0,padx=10,pady=5)
    horizontal_scrollbar = ttk.Scrollbar(root, orient="horizontal")
    horizontal_scrollbar.grid(row=8, column=1, sticky="ew",columnspan=2)
    content = tk.Text(root,width=70,height=10,wrap="none",xscrollcommand=horizontal_scrollbar.set)
    default_text = "Add your note here."
    content.insert("1.0", default_text)
    content.grid(row=6,column=1,padx=10,pady=5, rowspan=2, columnspan=2)
    horizontal_scrollbar.config(command=content.xview)

    addLineButton = ttk.Button(root,text="Add",command =lambda : add_Line_Button(chapter_entry,sub_entry,content,note_dict))
    addLineButton.grid(row=9,column=1,padx=10,pady=5 ,columnspan=2)

    submit_button = ttk.Button(root,text="make new note",command= lambda : make_note_button(content,[type_text_area.get(),dropdown_var.get()],projectNameInput.get(),givename(),note_dict,color_dictory)) 
    submit_button.grid(row=10, column=1, padx=10, pady=5,columnspan=2)                       # content,type_of_file,name, dict ={},colordict = {}  

    close_button = ttk.Button(root, text="Quit", command= lambda: close_window(root))
    close_button.grid(row=10, column=2, padx=10, pady=5,columnspan=2)

    root.mainloop()


if(__name__ == "__main__"):
    if(check_platform() == "Android"):
        show_welcome_android_page()
    else:
        show_welcome_page()
        current_file_name = os.getcwd()
