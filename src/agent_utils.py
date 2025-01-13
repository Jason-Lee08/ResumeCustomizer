import requests
from bs4 import BeautifulSoup

# TODO: Enable users to enter a link of a job description and extract the correct job description
def extract_text_from_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        text = soup.get_text(separator='\n')
        lines = [line.strip() for line in text.splitlines()]
        visible_text = '\n'.join(line for line in lines if line)

        return visible_text

    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching the webpage: {e}"