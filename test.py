import json 

data = {
    "name" : "g",
    "age" : 2,
    "language":["english","hindi"]
}

json_file_path = "test.json"
try:
    with open(json_file_path, 'r') as file:
        json_string = json.load(file)
        print(type(json_string))

except:
    with open(json_file_path, 'w') as file:
        json.dump({}, file, indent=4)

#with open(json_file_path,'w') as file:
 #   json.dump(data,file,indent=4)