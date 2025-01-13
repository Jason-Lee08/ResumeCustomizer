from jinja2 import Template, Environment, FileSystemLoader
import json
import os
import shutil
import subprocess
from time import sleep
from utils import *

env = Environment(
    loader=FileSystemLoader('.'),
    block_start_string='<<%',
    block_end_string='%>>',
    variable_start_string='<<',
    variable_end_string='>>'
)

script_dir = os.path.dirname(os.path.abspath(__file__))
latex_template_folder = os.path.join(script_dir, "resume_templates/resume_template_1/")

# Create backup folder
RESUME_BACKUP_FOLDER_PATH = os.path.join(script_dir, "../data/backups")
if not os.path.isdir(RESUME_BACKUP_FOLDER_PATH):
    os.mkdir(RESUME_BACKUP_FOLDER_PATH)

latex_folder_path = duplicate_new_src_folder(source_folder=latex_template_folder)
json_file_path = os.path.join(script_dir, "../data/final_result.json")

with open(json_file_path, 'r') as file:
    data = json.load(file)
print(f"New Dir: {latex_folder_path}")

resume_sections = ["education", "experience", "projects", "skills", "heading"]

for section_name in resume_sections[:3]:
    # json_file = os.path.join(JSON_FILE_DIR, f"{name}.json")
    latex_file = os.path.join(latex_folder_path, f"src/{section_name}.tex")

    # load the template
    with open(latex_file, "r") as file:
        template = env.from_string(file.read())

    if section_name == "experience":
        filled_tex = generate_experience(data, env)
    elif section_name == "projects":
        filled_tex = generate_projects(data, env)
    else:
        filled_tex = template.render(data[section_name])

    with open(latex_file, "w") as file:
        file.write(filled_tex)

    print(f"Filled {filled_tex} saved as {latex_file}")

# Get current working directory so we can revert later
cwd = os.getcwd()

# Sleep to allow the file op to complete
sleep(1)

if os.path.exists(latex_folder_path):
    os.chdir(latex_folder_path)
    print(f"Switched into {latex_folder_path}")
else:
    print(f"{latex_folder_path} does not exist")

print("Generating PDF...")
subprocess.call(f"pdflatex resume.tex".split(' '))

print(f"finished! returning to {cwd}")

if os.path.exists(cwd):
    os.chdir(cwd)
    print(f"Switched into {cwd}")
else:
    print(f"{cwd} does not exist")

print(f"moving resume to {cwd}")

newResumeLocation = os.path.join(latex_folder_path, 'resume.pdf')
newResumeDestination = os.path.join(cwd, "resume.pdf")

# If there is already a resume that exists and you want to backup previous resumes.
if os.path.exists(newResumeDestination):
    os.makedirs(RESUME_BACKUP_FOLDER_PATH, exist_ok=True)
    counter = 0
    while True:
        backup_name = f"resume_{counter}.pdf"
        backup_path = os.path.join(RESUME_BACKUP_FOLDER_PATH, backup_name)
        if not os.path.exists(backup_path):
            shutil.move(newResumeDestination, backup_path)     # move old resume from newResumeDestination to backup location
            print(f"Moved previous resume to backups folder as {backup_name}")
            break
        counter += 1

shutil.move(newResumeLocation, cwd)
shutil.rmtree(latex_folder_path)
print(f"new resume has been moved to {RESUME_BACKUP_FOLDER_PATH}/{cwd}")