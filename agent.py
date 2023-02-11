from dotenv import load_dotenv

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI

from commands import chrome_javascript_action, chrome_os_action

load_dotenv()

llm = OpenAI(temperature=0)

tools = load_tools([], llm=llm)

tools.append(chrome_os_action)
tools.append(chrome_javascript_action)

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

agent.run("Find me a good restaurant nearby")