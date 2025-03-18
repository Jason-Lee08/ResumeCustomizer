import json
import argparse
from groq import Groq
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

class ResumeGenerator:
    """
    Generates resumes based on user experience, projects, and a job description.
    Uses the Groq API to generate text-based resumes.
    """
    def __init__(self, groq_client):
        self.client = groq_client

    def generate_resume(self, experience, projects, job_description):
        """
        Generates a resume draft tailored to the given job description.
        
        Args:
            experience (str): User's past job experience.
            projects (str): User's relevant projects.
            job_description (str): The target job description.
        
        Returns:
            str: The generated resume.
        """
        prompt = ("Given the following job description and user experience, generate a customized resume draft.\n\n"
                  f"User Experience: {experience}\n\nProjects: {projects}\n\n"
                  f"Job Description: {job_description}")
        
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates professional resumes."},
                {"role": "user", "content": prompt}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7
        )
        return response.choices[0].message.content

class ResumeJudge:
    """
    Evaluates and compares resumes to determine the best one.
    Uses the Groq API to simulate a recruiter selecting the stronger candidate.
    """
    def __init__(self, groq_client):
        self.client = groq_client

    def evaluate_resumes(self, resume1, resume2):
        """
        Compares two resumes and selects the stronger candidate.
        
        Args:
            resume1 (str): The first resume.
            resume2 (str): The second resume.
        
        Returns:
            int: 1 if the first resume is better, 2 if the second resume is better.
        """
        prompt = ("Given the following resumes, select the stronger candidate. Respond with either 1 or 2.\n\n"
                  f"Candidate 1:\n{resume1}\n\n"
                  f"Candidate 2:\n{resume2}")
        
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert recruiter evaluating resumes."},
                {"role": "user", "content": prompt}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.5
        )
        return int(response.choices[0].message.content.strip())


class ResumeCoordinator:
    """
    Coordinates the resume generation and evaluation process.
    Creates multiple resumes and selects the best one using a tournament-style evaluation.
    """
    def __init__(self, groq_client, num_agents=2):
        self.groq_client = groq_client
        self.num_agents = num_agents
        self.generators = [ResumeGenerator(groq_client) for _ in range(num_agents)]
        self.judge = ResumeJudge(groq_client)
    
    def generate_resumes(self, experience, projects, job_description):
        """
        Generates multiple resumes using different resume generators.
        
        Args:
            experience (str): User's past job experience.
            projects (str): User's relevant projects.
            job_description (str): The target job description.
        
        Returns:
            list: A list of generated resumes.
        """
        resumes = [gen.generate_resume(experience, projects, job_description) for gen in self.generators]
        return resumes
    
    def select_best_resume(self, resumes):
        """
        Conducts a tournament-style battle to determine the best resume.
        
        Args:
            resumes (list): List of generated resumes.
        
        Returns:
            str: The best resume.
        """
        while len(resumes) > 1:
            new_round = []
            for i in range(0, len(resumes) - 1, 2):
                winner = resumes[i] if self.judge.evaluate_resumes(resumes[i], resumes[i+1]) == 1 else resumes[i+1]
                new_round.append(winner)
            if len(resumes) % 2 == 1:
                # Carry forward the last resume if odd count
                new_round.append(resumes[-1])
            resumes = new_round
        return resumes[0]
    
    def run(self, experience, projects, job_description):
        """
        Runs the entire resume generation and selection process.
        
        Args:
            experience (str): User's past job experience.
            projects (str): User's relevant projects.
            job_description (str): The target job description.
        
        Returns:
            str: The best resume selected from multiple candidates.
        """
        resumes = self.generate_resumes(experience, projects, job_description)
        best_resume = self.select_best_resume(resumes)
        return best_resume


def main(args):
    """
    Main function to load user data, generate resumes, and select the best one.
    
    Args:
        args: Command-line arguments.
    """
    with open(args.user_data_json, 'r') as f:
        user_data = json.load(f)
    
    with open(args.job_description_txt, 'r') as f:
        job_description = f.read()
    
    groq_client = Groq(api_key=GROQ_API_KEY)
    coordinator = ResumeCoordinator(groq_client)
    best_resume = coordinator.run(user_data['experience'], user_data['projects'], job_description)
    
    with open('best_resume.json', 'w') as f:
        json.dump({'best_resume': best_resume}, f, indent=4)
    print("Best resume saved as best_resume.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("user_data_json")
    parser.add_argument("job_description_txt")
    args = parser.parse_args()
    main(args)