import os
import re
import threading
import time
# start time
import copy

class VenvThread(threading.Thread):
    done = None

    def __init__(self, path_to):
        super().__init__()
        self.path_to = path_to

    def run(self) -> None:
        self.start = time.time()
        os.system(f'cd {self.path_to} && python -m venv venv')
        self.done_time = self.start - time.time()
        if self.__class__.done is None:
            self.__class__.done = self.done_time
        else:
            if self.__class__.done < self.done_time:
                self.__class__.done = self.done_time            

start = time.time()

def print(*args, **kwargs):
    os.system('cls' if os.name == 'nt' else 'clear')

    end = time.time()
    global start
    # time in minute and seconds and mili seconds
    past_time = end - start
    minute = int(past_time // 60)
    seconds = int(past_time % 60)

    __builtins__.print()
    __builtins__.print(f"Time taken: {minute:02d}:{seconds:02d}",
                       end = "\n\t")
    __builtins__.print(*args,
                       **kwargs)

# Read the markdown file
markdown_file = 'README.md'  # Replace with the path to your markdown file

# Open and read the content of the markdown file
with open(markdown_file,
          'r') as file:
    markdown_content = file.read()

# Extract project names and details
parts = markdown_content.split("##")
temp = []
tempelate = {
    "part": "",
    "sub_part": "",
    "project_names": []
    }
new_temp = tempelate.copy()

# Split the markdown content into sections
for p in parts:
    if p.startswith(" "):
        # New sub-section of projects detected, create a new template
        new_temp = tempelate.copy()
        new_temp["part"] = p.splitlines()[0]
    elif p.startswith("#"):
        # Project names and descriptions detected in the sub-section
        new_temp["sub_part"] = p.splitlines()[0][1:]
        new_temp["project_names"] = re.findall(r'(\d+)\.\s\**(.*?)\**:(.*)',
                                               p)
        temp.append(new_temp.copy())

# Print extracted project information for debugging purposes
print(*temp,
      sep = "\n")

# Create project folders
base_directory = 'Projects'  # Replace with the directory where you want to create the folders

# Create the base directory if it doesn't exist
os.makedirs(base_directory,
            exist_ok = True)
print(f'Created {base_directory}')
count = 0
temp = temp[1:]  # Skip the first template (assumed to be empty or non-project related)
threads = []

# Iterate through project information and create project folders
for parts in temp:
    project_directory = os.path.join(base_directory,
                                     parts["part"])

    # Create a sub-directory for the main project section
    os.makedirs(project_directory,
                exist_ok = True)

    project_directory = os.path.join(project_directory,
                                     parts["sub_part"])

    # Create a sub-directory for the sub-section within the main project section
    os.makedirs(project_directory,
                exist_ok = True)

    # Iterate through individual projects within the sub-section
    for project_name in parts["project_names"]:
        project_directory_f = os.path.join(project_directory,
                                           project_name[0] + "_" + project_name[1])

        # Create a folder for each project
        os.makedirs(project_directory_f,
                    exist_ok = True)
        __builtins__.print(f'Created {project_directory_f}')

        # Create README.md for each project with project name and description
        with open(os.path.join(project_directory_f,
                               'README.md'),
                  'w') as file:
            file.write(f'# {project_name[1]}')
            file.write("\n")
            file.write(project_name[2].strip())
            count += 1

        # Create empty requirements.txt and main.py files for each project
        with open(os.path.join(project_directory_f,
                               "requirements.txt"),
                  'w') as file:
            file.write("")
        with open(os.path.join(project_directory_f,
                               "main.py"),
                  'w') as file:
            file.write("")

        # Create a virtual environment (venv) in each project folder using threads
        threads.append(threading.Thread(target = os.system,
                                        args = (f'cd {project_directory_f} && python -m venv venv',)))
        threads[-1].start()

# Print the total number of folders created
print(f'{count} folders created in {base_directory}.')
print("Waiting for venv to be created by threads")
temp = 0

# Wait for threads to finish creating venv
while True:
    alives = []
    for t in threads:
        if t.is_alive() == True:
            alives.append(t)

    count_threads_alive = len(alives)
    if count_threads_alive == 0:
        break
    print(VenvThread.done)
    print("Alive threads count",
          count_threads_alive,
          f"\n\t ETA : {count_threads_alive * VenvThread.done if VenvThread.done is not None else 0:.2f} seconds")
    # Print the count of alive threads for monitoring
    if temp != count_threads_alive:
        print("Alive threads count",
              count_threads_alive,
              f"\n\t ETA : {count_threads_alive * VenvThread.done if VenvThread.done is not None else 0:.2f} seconds")
        temp = count_threads_alive

    # Exit the loop when all threads have finished

    time.sleep(1)