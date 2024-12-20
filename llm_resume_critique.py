"""
This script generates prompts an LLM agent to generate various different sample resumes 
for an inputted job description.

Once each agent is finished creating their resume, a different LLM agent system grades each resume, 
pretending to be a recruiter selecting the best candidate for the job description. This whole process is supervised
by another language model that critiques how realistic the resume is to avoid model drift. Another model verifies that the 
outputed resume uses data that the agent was actually given (to prevent hallucinations).

The best resume is chosen and returned to the user.
"""


system_prompt = """You are a career advisor with a stellar ability to write excellent, professional resumes for a user given a particular job description. 
Your job is to take in a particular job description and a collection of previous jobs/projects the user has worked on and output a resume that maximizes the likelihood of catching the recruiter's attention for this job description. 
The resume bullet points that you generate must fit within a single page. You may be prompted with feedback that you may need to shorten the resume to handle this.

You will first respond to a prompt asking you to draft a sample resume, based on which experiences/projects/skills you deem relevant for this job posting.

Please put the most relevant experiences at the top of each output. You will output in the following format:

{
    "experience": [
        {
            "company_name": "Example Company Name",
            "start_date": "Mar 2019",
            "end_date": "May 2020",
            "role_title": "Example ",
            "city": "Example City",
            "state": "EX",
            "bullet_points": [
                "Bullet 1",
                "Bullet 2",
            ]
        }
    ],
    "projects": [
        {
            "project_name": "Example Project",
            "skills": "example skill 1, example skill 2",
            "bullet_points": [
                "Bullet point 1",
                "Bullet point 2"
            ]        
        }
    ]
}

Please pick the most relevant 3 job experiences as well as 3 relevant projects, with up to (but not necessarily up to) 4 bullet points per item.
"""

def generate_recruiter_prompt(description, resume1, resume2):
    recruiter_sys_prompt = f"""
    You are a recruiter and you are hiring for a role with the following description: {description}

    Given the following resumes, pick the candidate with the better resume. Please respond with either 1 or 2.

    Candidate 1:
    {resume1}

    Candidate 2:
    {resume2}
    """
    return recruiter_sys_prompt

from autogen import ConversableAgent
import os
import dotenv
import json

NUM_AGENTS = 2

dotenv.load_dotenv()

def generate_first_prompt(userdata, job_description):
    return "Given the following job description and collection of user experiences and data, please output a draft of which experiences/projects/skills you would write on the user's resume.\n" + f"User Data: {userdata}\n\n" + f"Job Description: {job_description}"

coordinator_agent = ConversableAgent(
    name="Coordinator",
    system_message=system_prompt,
    llm_config={"config_list": [{"model": "gpt-4o-mini"}]},
    human_input_mode="NEVER",
)

builder_agents = []
for i in range(NUM_AGENTS):
    resume_builder_agent = ConversableAgent(
        name="Resume_Builder",
        system_message=system_prompt,
        llm_config={"config_list": [{"model": "gpt-4o-mini"}]},
        human_input_mode="NEVER",
    )
    builder_agents.append(resume_builder_agent)


job_descrption = ""
with open("microsoft_job_description.txt") as f:
    job_descrption = f.read()

with open("test_data.json", 'r') as f:
    userdata = json.load(f)

experience_project_skills = userdata['experience'] + userdata['projects']

chat_results = coordinator_agent.initiate_chats(
    [
        {
            "recipient": agent,
            "message": generate_first_prompt(userdata, job_descrption),
            "max_turns": 1,
        } for agent in builder_agents
    ]
)

def escape_json_string(json_string):
    result = json_string.replace('%', '\%')
    return result

with open("results.txt", 'w') as f:
    with open(f"results/result_{i}.json", 'w') as json_file:
        for i in range(len(chat_results)):
            f.write(str(chat_results[i]))
            f.write("\n\n\n")

            result = json.loads(escape_json_string(chat_results[i].chat_history[1]["content"]))
            json.dump(result, json_file, indent=4)


recruiter_agent = ConversableAgent(
    name="Job Recruiter",
    system_message=generate_recruiter_prompt(),
    llm_config={"config_list": [{"model": "gpt-4o-mini"}]},
    human_input_mode="NEVER",
)


print(chat_results)