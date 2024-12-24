import package as pk
import pandas as pd
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from tkinter import font
from flask import Flask, render_template,request,jsonify

def show_welcome_page(root):
    for widget in root.winfo_children():
        widget.destroy() 
    root.title("webnotes")
    root.config(background="black")
    main_frame = ttk.Frame(root, padding="10", borderwidth=2, relief="solid")
    main_frame.pack(fill='both', expand=False)
    custom_font = font.Font(family="Helvetica", size=25, weight="bold")
    ttk.Label(main_frame,text="Welcome to notesite",font=custom_font).grid(row=0,column=2,padx=10,pady=5)
    button_frame = ttk.Frame(root,padding=(20,5),borderwidth=2, relief="solid")
    # button_frame.grid(row=0, column=0, sticky="nsew")
    button_frame.pack(fill='both', expand=True)
    ttk.Button(button_frame, text= "make new note",command= lambda: show_UI_new_Project(root)).grid(row=1,column=1,padx=10,pady=5)
    # ttk.Button(button_frame, text="delete a note",command= lambda: delete_notesites(root)).grid(row=1,column=2,padx=20,pady=5)
    ttk.Button(button_frame, text="show all notesites",command= lambda: show_all_notesites(root)).grid(row=2,column=1,padx=20,pady=5)
    ttk.Button(button_frame, text="Quit", command=lambda: pk.ExitApp(root)).grid(row=2, column=2, padx=10, pady=5)
    root.mainloop()
    
    
def show_welcome_android_page(root):
    root.title("webnotes")
    root.config(background="black")

    main_frame = ttk.Frame(root, padding="10", borderwidth=2, relief="solid")
    main_frame.pack(fill='both', expand=False)
    custom_font = font.Font(family="Helvetica", size=20, weight="bold")
    ttk.Label(main_frame,text="Welcome to notesite",font=custom_font).grid(row=0,column=0,padx=0,pady=5)
    button_frame = ttk.Frame(root,padding=(20,5),borderwidth=2, relief="solid")
    button_frame.pack(fill='both', expand=True)
    ttk.Button(button_frame, text= "make new note",command= lambda: show_UI_new_Project(root)).grid(row=1,column=0,padx=20,pady=5)
    # ttk.Button(button_frame,text="delete a note",command=lambda: delete_notesites(root)).grid(row=1,column=1,padx=20,pady=5)
    ttk.Button(button_frame,text="show all notesites",command=lambda: show_all_notesites(root)).grid(row=2,column=0,padx=20,pady=5)
    ttk.Button(button_frame, text="Quit", command=lambda: pk.close_window(root)).grid(row=2, column=1, padx=20, pady=5)
    root.mainloop()


# def create_treeview(parent,cols,df):
#     tree = ttk.Treeview(parent,show="headings")
#     horizontal_scrollbar = ttk.Scrollbar(parent, orient="horizontal")
#     tree["columns"] = cols
#     for i in cols:
#         tree.column(i, anchor="w")
#         tree.heading(i, text=i, anchor='w')
#     for index, row in df.iterrows():
#         tree.insert("",tk.END,text=index,values=list(row))
#     tree.pack(padx=20,pady=0,fill=tk.BOTH, expand=True)
#     def on_item_select(event, tree):
#         selected_item = tree.focus()
#         if selected_item:
#             print(f"Selected Item in Tree {tree}: {tree.item(selected_item, 'text')}")
#             print("Hello, World!")
#     # Bind the selection event with lambda to pass the tree reference
#     tree.bind("<ButtonRelease-1>", lambda event: on_item_select(event, tree))
#     horizontal_scrollbar.pack()
#     return tree


def create_treeview(parent,cols,df):
    style = ttk.Style(parent)
    style.theme_use("alt")  

    # Customize the Treeview style
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="lightgray"
    )

    style.map("Treeview", background=[("selected", "blue")], foreground=[("selected", "white")])

    # Create a Treeview
    tree = ttk.Treeview(parent, columns=("Age", "Grade"), show="headings", height=5)
    tree["columns"] = cols
    # Define columns
    for i in cols:
        tree.column(i, anchor="w", width= 100)
        tree.heading(i, text=i, anchor='w')
    # Add data
    def on_item_select(event, tree):
        selected_item = tree.focus()
        if selected_item:
            actionRoot = tk.Tk()
            actionRoot.title(str(str(tree)[2:]))
            ttk.Button(parent, text="Edit", command=lambda: print("add function here")).pack()
            ttk.Button(parent, text="Delete", command=lambda: print("add function here")).pack()
            print(f"Selected Item in Tree {tree}: {tree.item(selected_item, 'text')}")

    for index, row in df.iterrows():
        tree.insert("", "end",text=index, values=list(row))

    # Pack the Treeview
    tree.pack(padx=10, pady=10)
    tree.bind("<ButtonRelease-1>", lambda event: on_item_select(event, tree))
    return tree

def show_all_notesites(root: type):
    root.title("all notes")
    for widget in root.winfo_children():
        widget.destroy() 
    DatabaseDict: list = [pk.DataBaseEntry(i) for i in pk.ReadFromDataBase(pk.databaseName,pk.noteTableName)]
    Set: set = set([ i.typeOf for i in DatabaseDict])
    dicts: dict = {key : [(list(i))[:-1] for i in DatabaseDict if i.typeOf == key] for key in Set}

    for i in dicts:
        # print(projects_dict,"   ",type(projects_dict))
        ttk.Label(root, text=i).pack(padx= 20)
        df = pd.DataFrame(list(dicts[i]),columns=["Number","name","SerialNumber","Date Created","Verision"])
        df.index = pd.Index(range(1, len(df) + 1))
        cols = list(df.columns)
        create_treeview(root,cols,df)
    ttk.Button(root, text="Back", command=lambda: show_welcome_page(root)).pack(padx=20,pady=30)
    root.mainloop()

def ShowFlaskWebNote(app,htmlAddress):
    @app.route('/')
    def hello_world():
        return render_template(htmlAddress)
    
    app.run(debug=True)


def DemoViewFrontEnd(demo_root): # this function is now not in use
    if demo_root is None:  # Check if root is None, meaning it hasn't been created yet
        demo_root.title("Demo")
        custom_font = font.Font(family="Helvetica", size=25, weight="bold")
        bold_font = ("Helvetica", 24, "bold")
        bold_font_h2 = ("Helvetica", 16, "bold")
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
                        
        demo_root.config(background="black")
        demo_root.mainloop()  

def show_UI_new_Project(root):
    for widget in root.winfo_children():
        widget.destroy() 
    root.title("Make New note")
    root.config(background="lightblue")

    main_frame = ttk.Frame(root, padding="10", borderwidth=2, relief="solid")
    main_frame.pack(fill='both', expand=True)
    label = ttk.Label(main_frame, text="Enter name of project:")
    label.grid(row=0, column=0, padx=10, pady=5)
    projectNameInput = ttk.Entry(main_frame,width=70)
    projectNameInput.grid(row=0, column=1, padx=10, pady=5,columnspan=2)
    
    color_dictory: dict = {}  
    note_dict: dict = {} 

    DDlabel = ttk.Label(main_frame,text = "choose the type:")
    DDlabel.grid(row=1,column=0,padx=10,pady = 5)
    type_text_area = ttk.Entry(main_frame,width=40)  
    type_text_area.grid(row=1,column=2)
    dropdown_var = tk.StringVar(main_frame)
    dropdown_var.set("None")  # Default value
    json_file_contant = [i[3] for i in pk.ReadFromDataBase(pk.databaseName,pk.noteTableName)]
    options = ["Choose Type"] + [*json_file_contant] + ["None"]
    
    dropdown_menu = ttk.OptionMenu(main_frame, dropdown_var, *options)
    dropdown_menu.grid(row=1, column=1, padx=10, pady=5) #pady = 50

    colorselect1 = ttk.Label(main_frame, text= "None")
    colorlabel = ttk.Label(main_frame, text="choose the text color:")
    colorlabel.grid(row=2,column=0,padx=10,pady=5)
    colorbutton = ttk.Button(main_frame, text="Choose Color", command= lambda: pk.ChooseColor1BackEnd(colorselect1,color_dictory))
    colorbutton.grid(row=2,column=1,padx=10,pady=5)
    colorselect1.grid(row=2,column=2,padx=15,pady=5)

    colorselect2 = ttk.Label(main_frame, text= "None")
    colorlabel = ttk.Label(main_frame, text="choose the backGround color:")
    colorlabel.grid(row=3,column=0,padx=10,pady=5)
    colorbutton = ttk.Button(main_frame, text="Choose Color", command= lambda: pk.ChooseColor2BackEnd(colorselect2,color_dictory))
    colorbutton.grid(row=3,column=1,padx=10,pady=5)
    colorselect2.grid(row=3,column=2,padx=15,pady=5)

    label = ttk.Label(main_frame, text="Enter Chapter Name:")
    label.grid(row=4, column=0, padx=10, pady=5)
    chapter_entry = ttk.Entry(main_frame,width=70)
    chapter_entry.grid(row=4, column=1, padx=10, pady=5,columnspan=2)

    label = ttk.Label(main_frame, text="Enter Sub-Chapter Name:")
    label.grid(row=5, column=0, padx=10, pady=5)
    sub_entry = ttk.Entry(main_frame,width=70)
    sub_entry.grid(row=5, column=1, padx=10, pady=5,columnspan=2)

    label = ttk.Label(main_frame, text = "Enter the content:")
    label.grid(row=6,column=0,padx=10,pady=5)
    horizontal_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal")
    horizontal_scrollbar.grid(row=8, column=1, sticky="ew",columnspan=2)
    content = tk.Text(main_frame,width=70,height=10,wrap="none",xscrollcommand=horizontal_scrollbar.set)
    default_text = "Add your note here."
    content.insert("1.0", default_text)
    content.grid(row=6,column=1,padx=10,pady=5, rowspan=2, columnspan=2)
    horizontal_scrollbar.config(command=content.xview)

    addLineButton = ttk.Button(main_frame,text="Add",command =lambda: pk.AddContentButton(chapter_entry,sub_entry,content,note_dict))
    addLineButton.grid(row=9,column=1,padx=10,pady=5 ,columnspan=2)

    submit_button = ttk.Button(main_frame,text="make new note",
        command= lambda: pk.MakeNoteButtonBackEnd(
                    content,
                    [type_text_area.get(),dropdown_var.get()],
                    projectNameInput.get(),
                    pk.givename(datetime),
                    note_dict,
                    color_dictory)) 
    submit_button.grid(row=10, column=1, padx=10, pady=5,columnspan=2)   

    back_button = ttk.Button(main_frame, text="Back", command= lambda: show_welcome_page(root))
    back_button.grid(row=10, column=2, padx=10, pady=5,columnspan=2)

    root.mainloop()