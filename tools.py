from langchain.agents.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.chains.base import Chain
from langchain.chains import LLMChain, SequentialChain

from commands import computer_action

applescript_prompt = PromptTemplate(
    input_variables=["command"],
    template="""
    Use this when you want to execute a command on the computer. The command should be in AppleScript.

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

    If you need to do a calculation, use the calculator app.

    Write the AppleScript for the Command:
    Command: {command}
    AppleScript: 
    """,
)

class AppleScriptExecutionChain(Chain):
    @property
    def input_keys(self):
        return ['applescript']

    @property
    def output_keys(self):
        return ['result']

    def _call(self, inputs):
        result = computer_action(inputs['applescript'])
        return {'output': result}

def make_computer_action_tool(llm):
    get_applescript_chain = LLMChain(llm=llm, prompt=applescript_prompt)

    AppleScriptExecutionChain()

    sequential_execute = SequentialChain(
            chains=[get_applescript_chain,
            ]
    )

    return Tool(
        name="Computer Action",
        description="Useful for when you need to do an action on the computer.",
        func=sequential_execute.run,
    )

javascript_prompt = PromptTemplate(
    input_variables=["command"],
    template="""
    Use this when you want to execute a command on Chrome. The command should be Javascript and will run in the active window.

    Here are some examples of good Javascript commands:

    Command: Get the links on the page
    Javascript: document.getElementsByTagName("a")

    Command: Get the buttons on the page
    Javascript: document.getElementsByTagName("button")

    Write the Javascript for the Command:
    Command: {command}
    Javascript: 
    """,
)

def make_chrome_action_tool(llm):
    chain = LLMChain(llm=llm, prompt=javascript_prompt)

    return Tool(
        name="Chrome Action",
        description="Useful for when you need to do an action on the current page in Chrome.",
        func=chain.run,
    )