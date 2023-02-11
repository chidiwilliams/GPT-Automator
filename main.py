# import load_dotenv
import sys

from dotenv import load_dotenv

from langchain import PromptTemplate
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI

from commands import action

# load environment variables
load_dotenv()

def main(command):
    # First, let's load the language model we're going to use to control the agent.
    llm = OpenAI(temperature=0.9)

    prompt = f"""
    I want you to generate the AppleScript to execute a command.

    Here are some examples of good AppleScript commands:

    Command: Create a new page in Notion
    AppleScript: tell application "Notion"
        activate
        delay 0.5
        tell application "System Events" to keystroke "n" using {{command down}}
    end tell

    Command: Search for a table nearby
    AppleScript: tell application "Google Chrome"
    activate
    open location "https://www.google.com/search?q=Table+nearby"
    end tell

    The AppleScript should be valid and when appropriate use keyboard shortcuts.

    Write the AppleScript for the Command: {command}?
    """

    applescript = llm(prompt)

    print("Prompt: ", applescript)

    applescript = applescript.replace("AppleScript: ", "")

    action(applescript)

if __name__ == "__main__":
    command = sys.argv[1]
    if not command:
        print("Please provide a command to execute e.g. python main.py 'Open the calculator app'")
        exit(1)

    main(command)
