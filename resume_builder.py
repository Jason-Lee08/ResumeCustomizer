from jinja2 import Template, Environment, FileSystemLoader
import json
import os
import shutil

env = Environment(
    loader=FileSystemLoader('.'),
    block_start_string='<<%',
    block_end_string='%>>',
    variable_start_string='<<',
    variable_end_string='>>'
)

def generate_experience(data):
    """
    Given information about multiple job experiences in a JSON format, this function will output the LaTeX formatted file for all experiences by iterating over each entry and generating corresponding LaTeX code.

    Args:
        data (dict): A JSON object containing experience information.

    Returns:
        str: The LaTeX formatted experience section.
    """
    # Template for the experience section
    template = """%-----------EXPERIENCE-----------%
\\section{Experience}
\\resumeSubHeadingListStart

{all_experiences}
\\resumeSubHeadingListEnd
"""

    experience_template = """
    \\resumeSubheading
    {<<company_name>>}{<<start_date>> -- <<end_date>>}
    {<<role_title>>}{<<city>>, <<state>>}
    \\resumeItemListStart
<<bullet_items>>
    \\resumeItemListEnd
    """

    all_experiences = ""

    for exp in data.get("experience", []):
        # Extract details for each experience
        context = {
            "company_name": exp.get("company_name", "Company Name"),
            "start_date": exp.get("start_date", ""),
            "end_date": exp.get("end_date", ""),
            "role_title": exp.get("role_title", "Role Title"),
            "city": exp.get("city", "City"),
            "state": exp.get("state", "State"),
            "bullet_items": "".join(["        \\resumeItem{%s}\n" % bullet for bullet in exp.get("bullet_points", ["Bullet point 1", "Bullet point 2"])]),
        }

        # Render the experience template with context
        experience_section = env.from_string(experience_template).render(context)
        all_experiences += experience_section

    # Render the main template with the combined experiences
    final_output = template.replace("{all_experiences}", all_experiences)

    return final_output

def duplicate_new_src_folder(source_folder="resume", subfolder="resume_folder"):
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return

    i = 0
    while True:
        if subfolder != "":
            target_folder = os.path.join(subfolder, f"resume{i}")
        if not os.path.exists(target_folder):
            # Create the target folder
            os.makedirs(target_folder)
            print(f"Created folder: {target_folder}")

            # Copy the contents of 'src' to the new folder
            shutil.copytree(source_folder, target_folder, dirs_exist_ok=True)
            print(f"Copied contents from '{source_folder}' to '{target_folder}'")
            break
        i += 1

    return target_folder

def generate_projects(data):
    """
    Given information about multiple job experiences in a JSON format, this function will output the LaTeX formatted file for all experiences by iterating over each entry and generating corresponding LaTeX code.

    Args:
        data (dict): A JSON object containing experience information.

    Returns:
        str: The LaTeX formatted experience section.
    """
    # Template for the experience section
    template = """%-----------PROJECTS-----------%
\\section{Projects}
\\resumeSubHeadingListStart

<<project_data>>

\\resumeSubHeadingListEnd
"""

    project_template = """
    \\resumeProjectHeading
    {\\textbf{<<project_name>>} $|$ \emph{<<skills>>}}    {}
    \\resumeItemListStart
        <<bullet_items>>
    \\resumeItemListEnd
    """

    all_experiences = ""

    for exp in data.get("projects", []):
        # Extract details for each experience
        context = {
            "project_name": exp.get("project_name", "Project"),
            "skills": exp.get("skills", ""),
            "bullet_items": "".join(["        \\resumeItem{%s}\n" % bullet for bullet in exp.get("bullet_points", ["Bullet point 1", "Bullet point 2"])]),
        }

        # Render the experience template with context
        experience_section = env.from_string(project_template).render(context)
        all_experiences += experience_section

    # Render the main template with the combined experiences
    final_output = template.replace("<<project_data>>", all_experiences)

    return final_output

def duplicate_new_src_folder(source_folder="resume", subfolder="resume_folder"):
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return

    i = 0
    while True:
        if subfolder != "":
            target_folder = os.path.join(subfolder, f"resume{i}")
        if not os.path.exists(target_folder):
            # Create the target folder
            os.makedirs(target_folder)
            print(f"Created folder: {target_folder}")

            # Copy the contents of 'src' to the new folder
            shutil.copytree(source_folder, target_folder, dirs_exist_ok=True)
            print(f"Copied contents from '{source_folder}' to '{target_folder}'")
            break
        i += 1

    return target_folder

TEMP_DIR = duplicate_new_src_folder()
JSON_FILE = "result_0.json"

with open(JSON_FILE, 'r') as file:
    data = json.load(file)
print(f"New Dir: {TEMP_DIR}")
resume_sections = ["education", "experience", "projects", "skills", "heading"]

for section_name in resume_sections[:3]:
    # json_file = os.path.join(JSON_FILE_DIR, f"{name}.json")
    latex_file = os.path.join(TEMP_DIR, f"src/{section_name}.tex")

    # load the template
    with open(latex_file, "r") as file:
        template = env.from_string(file.read())

    if section_name == "experience":
        filled_tex = generate_experience(data)
    elif section_name == "projects":
        filled_tex = generate_projects(data)
    else:
        filled_tex = template.render(data[section_name])

    with open(latex_file, "w") as file:
        file.write(filled_tex)

    print(f"Filled {filled_tex} saved as {latex_file}")



