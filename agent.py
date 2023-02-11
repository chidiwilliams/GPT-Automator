from dotenv import load_dotenv

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI

from commands import chrome_javascript_action, computer_applescript_action

load_dotenv()

llm = OpenAI(temperature=0)

tools = [
    computer_applescript_action,
    chrome_javascript_action,
    
]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

agent.run("Find me a great restaurant for tonight")
# agent.run("What is 5 x 5?")
# agent.run("Play a game of chess")
# agent.run("Find me a table nearby")

