import os
import json
import package as pk
from flask import Flask#,render_template,jsonify
from flask_sqlalchemy import SQLAlchemy


# Connect to the database
# connection = sqlite3.connect('example.db')

# # Create a cursor object
# cursor = connection.cursor()

# # Execute a SELECT query
# cursor.execute("SELECT * FROM my_table")

# # Fetch all rows
# rows = cursor.fetchall()

# # Iterate through the rows and print them
# for row in rows:
#     print(row)

# # Close the connection
# connection.close()

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
# db=SQLAlchemy(app)
# @app.route('/')
# def hello_world():
#     addThis = first(name = "second",classof = "tweleth")
#     db.session.add(addThis)
#     db.session.commit()
#     return render_template('index.html')
#     return "good morning new world"

# if __name__ == "__main__":
#     app.run(debug=True)


class file_info:
    def __init__(self,fileName,version):
        self.file_name = str(fileName)
        self.file_number_base64 = givename(pk.datetime)
        self.version = version
        self.color_dict = {}
        self.chapter_dict = {}

    def changeFilename(self,name) -> None:
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
        "webnote_version" : str(pk.current_verision),
        "colors" : note_class_object.color_dict,
        "content" : note_class_object.chapter_dict
    }}  

def JsonObject(typeOfFile,name,current_verision,color_dict = {}, dict ={}):
    fileObject = file_info(name,current_verision)
    fileObject.changeColorDict(color_dict)
    fileObject.AddDictDrictly(dict)
    json_file_data = pk.ReadFromDataBase(pk.databaseName,pk.noteTableName)

    pk.AddDatabaseEntry(pk.databaseName,pk.noteTableName,(fileObject.file_number_base64,name,
            typeOfFile,f"{pk.datetime.now().day}/{pk.datetime.now().month}/{pk.datetime.now().year}",str(dict)))  
    # try:
    #     json_file_data[type_of_file].update(make_class_dict(fileObject))
    # except:
    #     json_file_data[type_of_file] = {}
    #     json_file_data[type_of_file].update(make_class_dict(fileObject))
        
    return json_file_data


def read_the_json(json_file_path):  #leagcy function
    with open(json_file_path, 'r') as file:
        json_var = json.load(file)
    return json_var
       
def write_the_json(json_file_path,data={}): # Leagcy function
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def givename(current_time):
    info_dict = pk.ReadFromDataBase(pk.databaseName,pk.noteTableName)
    day = current_time.now().day
    month = current_time.now().month
    year = current_time.now().year
    firstpart = pk.base10_to_base64(day) + pk.base10_to_base64(month) + pk.base10_to_base64(year)
    # projects = 0
    # for i in info_dict:
    #     projects += len(info_dict[i]) + 1
    projects = len(info_dict) + 1
    secondpart = str(projects)
    return firstpart + secondpart

def make_html_file(filename,filenumber,file_directory_path,dict_of_chapter = {},colordict = {}):
    # Create the directory if it doesn't exist
    if not os.path.exists(file_directory_path):
        os.mkdir(file_directory_path)
    else:
        # replace the content of file
        pass

    # Define the HTML content
    with open("static/index.html") as file:
        html_content = file.read() # left here 29/11/2024
        html_content = html_content.replace('"MainDict/**/"',str(dict_of_chapter))
        print(colordict)
        html_content = html_content.replace("TextColor/**/",str(colordict["text-color"]))
        html_content = html_content.replace("Background_Color/**/",str(colordict["background-color"]))
        html_content = html_content.replace("ProjectName/**/",filename)
        html_content = html_content.replace("ProjectFileNumber/**/",filenumber)
    
    # Define the file path
    file_path = os.path.join(file_directory_path, filename)
    os.makedirs(file_path, exist_ok=True)
    html_file = os.path.join(file_path,"index.html")
    pictureFile = os.path.join(file_path,"pics")    
    try:
        with open(html_file, 'w') as file:
            file.write(html_content)
    except:
        print("something went wrong.")
    return html_file

def make_all_line_in_note(text): # make dict
    manlist = []
    alllines = text.split("\n")
    for i in range(len(alllines)):
        alllines[i] = alllines[i].rstrip()
    indexNumber = 0
    for i in alllines:
        a = i.replace("?","").replace("|","").strip()
        if a in pk.notesiteTag:
            lineplace = alllines.index(f"|{a}?")
            lineEnd = alllines.index(f"|/{a}?")
            manlist.append({"type" : a,"text" : alllines[lineplace:(lineEnd+1)],"place":lineplace-1+indexNumber})
            indexNumber += 1
            for i in alllines[lineplace:(lineEnd+1)]:
                del alllines[alllines.index(i)]
    for i in alllines:  # if normal text
        alllines[alllines.index(i)] = {"type": "text","text": i}
    
    linofdict = 0
    for i in manlist:
        alllines.insert(i["place"] + 1,manlist[linofdict])
        linofdict += 1
     
    return alllines 

def make_dataFrame_dict(dict) -> dict:
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

