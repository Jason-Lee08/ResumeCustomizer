"""
This script generates prompts an LLM agent to generate various different sample resumes 
for an inputted job description.

Once each agent is finished creating their resume, a different LLM agent system grades each resume, 
pretending to be a recruiter selecting the best candidate for the job description. This whole process is supervised
by another language model that critiques how realistic the resume is to avoid model drift. Another model verifies that the 
outputed resume uses data that the agent was actually given (to prevent hallucinations).

The best resume is chosen and returned to the user.
"""
import dotenv
import json
import openai
from resume_agents.agents import *
import argparse

NUM_AGENTS = 2

dotenv.load_dotenv()

def generate_first_prompt(user_experience, user_projects, job_description):
    return "Given the following job description and collection of user experiences and data, please output a draft of which experiences/projects/skills you would write on the user's resume.\n\n" + f"Here is the user's previous career experience: {user_experience}\n\nHere is the user's projects (that may or may not be relevant): {user_projects}.\n\n Here is the job description that you will customize the resume for: {job_description}"

def generate_recruiter_system_prompt(description):
    recruiter_sys_prompt = f"""
    You are a recruiter and you are hiring for a role with the following description: {description}
    """
    return recruiter_sys_prompt

def search_for_keywords(text, keywords):
    """
    Keywords 
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an assistant who processes text from webpages. Please respond with the identified content and nothing else. For example, please don't start with \"Here is the desired content: \". "},
            {"role": "user", "content": f"Find relevant information about '{", ".join(keywords)}' in the following text:\n\n{text}"}
        ]
    )

    return response


def generate_recruiter_message_prompt(resume1, resume2):
    result = f"""
        Given the following resumes, pick the candidate with the better resume. Please respond with either 1 or 2.

    Candidate 1:
    {resume1}

    Candidate 2:
    {resume2}
    """
    return result



def escape_json_string(json_string):
    " Applied before serializing responses to json so that they can be loaded in by Python "
    result = json_string.replace('%', '%')
    return result

class Resume_Evaluator:
    
    def __init__(self):
        # TODO: initialize client (GROQ)
        pass

    def evaluate_resume(self, resume1, resume2):
        """
        Input: Two potential resumes, both in JSON format.

        Outputs: Either resume1 or resume2, depending on what the evaluator model decides.
        """
        system_prompt = self._generate_recruiter_message_prompt(resume1, resume2)

        # TODO: call the model API to get the answer. Please add any additional API calls or functionality to ensure the answer is clear


    def _generate_recruiter_message_prompt(self, resume1, resume2):
        result = f"""
    Given the following resumes, pick the candidate with the better resume. Please respond with either 1 or 2.

    Candidate 1:
    {resume1}

    Candidate 2:
    {resume2}
    """
        return result

def resume_battle(resume1, resume2, MAX_BATTLES=3):
    """
    This function uses a resume evaluator agent to pick the best resume.
    To ensure ordering doesn't matter, it will ask the evaluator two times.
    If both there is a tie, then more iterations of this process are sampled,
    until a maximum of MAX_BATTLES battles have occured. 
    """
    # TODO:
    return

def recursive_battle(data, num_battles=1):
    """
    Given the user's information contained in data, which is a JSON file with the following formats:

    
    num_battles - number of battles to recursively call, should be a multiple of 2

    This function should create `num_battles` resume battles where it functions similar to a tournament bracket.
    A judge model determines the best resume.

    Utilizing the Groq API, please create two generations and then use a judge model that selects the best resume.
    Please create a helper function called judge_resume(resume1, resume2). 
    This should take in two resumes and pass them to a judge model and ask them which one is better. 
    Please make the system prompt for this model blank (I will make sure it does not do that)
    """
    # TODO
    return

def build_resume(user_previous_experience, user_projects, job_descrption):
    """
    This function creates a feedback loop using a resume builder and a feedback agent.
    """
    # TODO: create a resume builder agent and a resume critique agent for feedback that uses reasoning
    feedback_agent = getFeedbackAgent()
    builder_agent = getResumeBuilderAgent()
    
    chat_results = feedback_agent.initiate_chats(
        [
            {
                "recipient": builder_agent,
                "message": generate_first_prompt(user_previous_experience, user_projects, job_descrption),
                "max_turns": 1,
                "summary_method": "last_msg",
            }
        ]
    )

    return chat_results

USERDATA_MAINTAIN_KEYS = ["education"]

def main(args):
    """
    This function creates N agents that each build their own resume, so N resumes total.
    Then, another agent critiques the resume, giving back-and-forth dialogue.
    After this process is completed, an evaluator agent critiques each resume in a face-off manner.
    """

    # parse args
    print(f"Args: {args}")
    job_descrption_txt_file = args.job_description_txt
    user_data_json_file = args.user_data_json

    # Load the files
    with open(user_data_json_file, 'r') as f:
        all_user_data = json.load(f)
        user_data_experience = all_user_data['experience']
        user_data_projects = all_user_data['projects']
        result_dict = {key:all_user_data[key] for key in USERDATA_MAINTAIN_KEYS}
        

    # TODO: in the future, use AI to parse the job description/anything relevant from the user inputted URL
    with open(job_descrption_txt_file, 'r') as f:
        job_description = f.read()

    # coordinator asks each resume agent to build chat
    resume_results = build_resume(user_data_experience, user_data_projects, job_description)

    with open('data/results.txt', 'w') as f:
        for i in range(len(resume_results)):
            f.write(resume_results[i].chat_history[i]["content"])
            f.write("\n\n\n")

    with open('data/final_result.txt', 'w') as f:
        f.write(str(resume_results[-1].chat_history[-1]["content"]))

    with open('data/final_result.json', 'w') as f:
        escaped_final_resume = escape_json_string(resume_results[-1].chat_history[-1]["content"])
        print("4" * 50)
        print(escaped_final_resume)
        results = json.loads(escaped_final_resume)
        result_dict.update(results)
        json.dump(result_dict, f, indent=4)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("user_data_json")
    parser.add_argument("job_description_txt")
    main(parser.parse_args())