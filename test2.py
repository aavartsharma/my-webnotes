import os

file_path = "new"
if not os.path.exists(file_path):
    os.mkdir(file_path)
    print(f'Directory {file_path} created successfully.')
file_paths = os.path.join(file_path, 'gta')
os.makedirs(file_paths,exist_ok=True)
file_pathss = os.path.join(file_paths,"gtaa.html")
with open(file_pathss, 'w') as file:
    file.write("html_content")
# os.path.join(file_paths,"h.html")