import os
import package as pk
import webbrowser as wb
import tkinter as tk
from tkinter import messagebox
from tkinter import colorchooser

def MakeNoteButtonBackEnd(content,type_of_file,name,filenumber, dict ={},colordict = {}): # for diplaying message
    # user_text = content.get("1.0",tk.END)
    typeofNote = ""
    if(type_of_file[0] == ""):
        typeofNote = type_of_file[1]
    else:
        typeofNote = type_of_file[0]
    pk.JsonObject(typeofNote,name,pk.current_verision,colordict,dict)
    if('templates' not in os.listdir()):
        pk.os.makedirs('templates')
    file_path_html_created = pk.make_html_file(name,filenumber,os.getcwd() + "\\templates\\notes" ,dict,colordict)
    if messagebox.askyesno("Open", "The file was made successfully.\n Do you want to open the notesite?"):
        wb.open(file_path_html_created) 
    else:
        pass

def ExitApp(root):
    if messagebox.askyesno("Close", "Are you sure you want \nto close the window?"): root.destroy()

def ChooseColor1BackEnd(colorselect,color_dict = {}):
    color_code = colorchooser.askcolor(title = "Choose a color")
    if (None not in color_code):
        colorselect.config(text= '             ')
        colorselect.config(background = f"{color_code[1]}")
        color_dict["text-color"] = str(color_code[1])
        return str(color_code)

def ChooseColor2BackEnd(colorselect,color_dict = {}):
    color_code = colorchooser.askcolor(title = "Choose a color")
    if (None not in color_code):
        colorselect.config(text= '             ')
        colorselect.config(background = f"{color_code[1]}")
        color_dict["background-color"] = str(color_code[1])
        return str(color_code)
    
def AddContentButton(chapter,sub_chapter,text,dict):
    chapter_name = chapter.get()
    sub_chapter_name = sub_chapter.get()
    content_text = text.get("1.0",tk.END)
    list_of_notes = pk.make_all_line_in_note(content_text)
    try:
        dict[chapter_name].update({sub_chapter_name:list_of_notes})
    except:
        dict[chapter_name] = {}
        dict[chapter_name].update({sub_chapter_name:list_of_notes})

    # DemoViewFrontEnd()  not in use anymore 