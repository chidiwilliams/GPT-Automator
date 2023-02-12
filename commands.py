import subprocess
import re

from langchain.agents import tool

@tool
def computer_applescript_action(apple_script):
    """
    Use this when you want to execute a command on the computer. The command should be in AppleScript.

    Always start with starting the app and activating it.

    If it's a calculation, use the calculator app.

    Use delay 0.5 between keystrokes.

    When possible click buttons instead of typing.

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
        delay 0.5
        open location "https://www.google.com/search?q=Table+nearby"
    end tell

    The AppleScript should be valid including quotations.

    Write the AppleScript for the Command:
    Command: 
    """
    print("Running\n", apple_script)

    return run_applescript(apple_script)

@tool
def chrome_get_the_links_on_the_page(input):
    """
    Use this when you want to get the links on the current page.

    You should use this before clicking on anything
    """
    return run_javascript('Array.from(document.querySelectorAll("a")).map(x => x.innerText + ": " + x.href).join(" - ")')[:4000]

@tool
def chrome_click_on_link(link):
    """
    Use this when you want to go to a link. 
    
    The link should be a url from a previous observation
    """
    return run_javascript(f'window.location.href = "{link}"')[:4000]

@tool
def chrome_read_the_page(input):
    """
    Use this when you want to read the page.
    """

    return run_javascript('document.body.innerText')[:4000]


# @tool
# def chrome_javascript_action(javascript):
#     """
#     Use this when you want to execute a javascript command on Chrome either to get data or trigger an action. The command should be in Javascript.

#     Here are some examples of good Javascript commands:

#     Command: Get the links on the page
#     document.querySelectorAll('a')

#     Command: Get the buttons on the page
#     document.querySelectorAll('button')

#     Command: Click the first button on the page
#     document.querySelectorAll('button')[0].click()

#     Write the Javascript for the command:
#     """

#     stdout = run_javascript(javascript)

#     return f"""
#     Current URL: {run_javascript('window.location.href')}

#     Result: {stdout}
#     """

@tool
def chrome_open_url(url):
    """
    Use this tool to open a URL in Chrome. It is recommended to use this tool before doing any other actions on Chrome.
    
    The URL should be a string. For example: https://gmail.com
    """
    script = f'''
    tell application "Google Chrome"
        open location "{url}"
    end tell
    '''

    return run_applescript(script)

def run_javascript(javascript):
    javascript = javascript.replace('"', '\\"')

    if javascript.startswith('open '):
        return "Invalid command, not javascript"

    script = f'''
    tell application "Google Chrome"
        tell active tab of front window
            execute javascript "{javascript}"
        end tell
    end tell
    '''
    
    return run_applescript(script)

def run_applescript(applescript):
    p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = p.communicate(applescript.encode('utf-8'))

    if p.returncode != 0:
        raise Exception(stderr)

    decoded_text = stdout.decode("utf-8")

    return decoded_text


def say_text(text):
    run_applescript(f'say "{text}"')
