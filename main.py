import sys

from dotenv import load_dotenv

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI

from commands import chrome_click_on_link, chrome_get_the_links_on_the_page, chrome_open_url, chrome_read_the_page, computer_applescript_action, say_text


# load environment variables
load_dotenv()

def main(command):
    llm = OpenAI(temperature=0)

    tools = [
        computer_applescript_action,
        chrome_open_url,
        chrome_get_the_links_on_the_page,
        chrome_click_on_link,
        chrome_read_the_page
    ]

    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

    result = agent.run(command)

    if result:
        say_text(f'The result is {result}')
    else:
        say_text(f'Finished doing {command}')

if __name__ == "__main__":
    command = sys.argv[1]
    if not command:
        print("Please provide a command to execute e.g. python main.py 'Open the calculator app'")
        exit(1)

    main(command)
