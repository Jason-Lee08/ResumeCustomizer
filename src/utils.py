import os
import shutil

def generate_experience(data, env):
    """
    Given information about multiple job experiences in a JSON format, this function will output the LaTeX formatted file for all experiences by iterating over each entry and generating corresponding LaTeX code.

    Args:
        data (dict): A JSON object containing experience information.

    Returns:
        str: The LaTeX formatted experience section.
    """
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
        context = {
            "company_name": exp.get("company_name", "Company Name"),
            "start_date": exp.get("start_date", ""),
            "end_date": exp.get("end_date", ""),
            "role_title": exp.get("role_title", "Role Title"),
            "city": exp.get("city", "City"),
            "state": exp.get("state", "State"),
            "bullet_items": "".join(["        \\resumeItem{%s}\n" % add_escape_chars(bullet) for bullet in exp.get("bullet_points", ["Bullet point 1", "Bullet point 2"])]),
        }

        experience_section = env.from_string(experience_template).render(context)
        all_experiences += experience_section

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
            os.makedirs(target_folder)
            print(f"Created folder: {target_folder}")

            shutil.copytree(source_folder, target_folder, dirs_exist_ok=True)
            print(f"Copied contents from '{source_folder}' to '{target_folder}'")
            break
        i += 1

    return target_folder

def add_escape_chars(json_string):
    " Applied before serializing responses to json so that they can be loaded in by Python "
    result = json_string.replace('%', '\\%')
    return result

def generate_projects(data, env):
    """
    Given information about multiple job experiences in a JSON format, this function will output the LaTeX formatted file for all experiences by iterating over each entry and generating corresponding LaTeX code.

    Args:
        data (dict): A JSON object containing experience information.

    Returns:
        str: The LaTeX formatted experience section.
    """

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
        context = {
            "project_name": exp.get("project_name", "Project"),
            "skills": exp.get("skills", ""),
            "bullet_items": "".join(["\\resumeItem{%s}\n" % add_escape_chars(bullet) for bullet in exp.get("bullet_points", ["Bullet point 1", "Bullet point 2"])]),
        }

        experience_section = env.from_string(project_template).render(context)
        all_experiences += experience_section

    final_output = template.replace("<<project_data>>", all_experiences)

    return final_output

def duplicate_new_src_folder(source_folder="resume", subfolder="./"):
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return

    i = 0
    while True:
        if subfolder != "":
            target_folder = os.path.join(subfolder, f"resume{i}")
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            print(f"Created folder: {target_folder}")

            shutil.copytree(source_folder, target_folder, dirs_exist_ok=True)
            print(f"Copied contents from '{source_folder}' to '{target_folder}'")
            break
        i += 1

    return target_folder

