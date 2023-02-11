from dotenv import load_dotenv

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI

from commands import computer_action, chrome_open_url, get_url_compose_gmail, chrome_action

load_dotenv()

llm = OpenAI(temperature=0.1)

tools = load_tools([], llm=llm)

tools.append(computer_action)
tools.append(chrome_open_url)
tools.append(get_url_compose_gmail)
tools.append(chrome_action)

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True,max_iterations=10)

#agent.run("Search for a table nearby")
#agent.run("Open outlook, wait a second and create a new email")
agent.run("Create a new email to tim_beans@hotmail.com in Chrome")
#agent.run("go to bbc.com and, once there, execute the javascript to print 'haha' in chrome")
