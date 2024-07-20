import os

# Define the directory path
directory_path = 'my_html_folder'

# Create the directory if it doesn't exist
if not os.path.exists(directory_path):
    os.mkdir(directory_path)
    print(f'Directory {directory_path} created successfully.')

# Define the HTML content
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My HTML File</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>This is my HTML file created using Python.</p>
</body>
</html>
'''

# Define the file path
file_path = os.path.join(directory_path, 'h.html')

# Write HTML content to the new file
with open(file_path, 'w') as file:
    file.write(html_content)

print(f'HTML file {file_path} created successfully.')
