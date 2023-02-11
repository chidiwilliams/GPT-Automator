from dotenv import load_dotenv

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI

from commands import computer_action

load_dotenv()

llm = OpenAI(temperature=0)

tools = load_tools([], llm=llm)

tools.append(computer_action)

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

agent.run("What is 5 times 5?")