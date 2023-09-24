import os
import re

# Read the markdown file
markdown_file = 'README.md'  # Replace with the path to your markdown file
with open(markdown_file, 'r') as file:
    markdown_content = file.read()

# Extract project names
parts = markdown_content.split("##")
temp = []
tempelate = {"part": "","sub_part":"", "project_names": []}
new_temp = tempelate.copy()
for p in parts:
    if p.startswith(" "):
        new_temp = tempelate.copy()
        new_temp["part"] = p.splitlines()[0]
    elif p.startswith("#"):

        new_temp["sub_part"] = p.splitlines()[0][1:]
        new_temp["project_names"] = re.findall(r'(\d+)\.\s\**(.*?)\**:(.*)', p)
        temp.append(new_temp.copy())
print(*temp, sep="\n")
# Create folders
base_directory = 'Projects'  # Replace with the directory where you want to create the folders
os.makedirs(base_directory, exist_ok=True)
print(f'Created {base_directory}')
count = 0
temp = temp[1:]
for parts in temp:
    project_directory = os.path.join(base_directory, parts["part"])
    os.makedirs(project_directory, exist_ok=True)
    project_directory = os.path.join(project_directory, parts["sub_part"])
    os.makedirs(project_directory, exist_ok=True)

    for project_name in parts["project_names"]:
        project_directory_f = os.path.join(project_directory, project_name[0]+"_"+project_name[1])
        os.makedirs(project_directory_f, exist_ok=True)
        print(f'Created {project_directory_f}')
        with open(os.path.join(project_directory_f, 'README.md'), 'w') as file:
            file.write(f'# {project_name[1]}')
            file.write("\n")
            file.write(project_name[2].strip())
            count += 1
        with open(os.path.join(project_directory_f,"requirements.txt"), 'w') as file:
            file.write("")

print(f'{count} folders created in {base_directory}.')


