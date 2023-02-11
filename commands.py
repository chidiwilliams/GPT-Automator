import subprocess

from langchain.agents import tool

@tool
def computer_applescript_action(apple_script):
    """
    Use this when you want to execute a command on the computer. The command should be in AppleScript.

    Always start with starting the app and activating it.

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
    Command: 
    """
    print("Running\n", apple_script)

    p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(apple_script.encode('utf-8'))

    if p.returncode != 0:
        raise Exception(stderr)

    return stdout

@tool
def chrome_javascript_action(javascript):
    """
    Use this when you want to execute a javascript command on Chrome either to get data or trigger an action. The command should be in Javascript.

    Here are some examples of good Javascript commands:

    Command: Get the links on the page
    document.querySelectorAll('a')

    Command: Get the buttons on the page
    document.querySelectorAll('button')

    Command: Click the first button on the page
    document.querySelectorAll('button')[0].click()

    Write the Javascript for the command:
    """
    p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
    stdout, stderr = p.communicate(script.encode('utf-8'))

    if p.returncode != 0:
        raise Exception(stderr)

    return f"""
    Current URL: {run_javascript('window.location.href')}

    Result: {stdout}
    """

@tool
def chrome_open_url(url):
    """
    Use this tool to open a URL in Chrome. It is recommended to use this tool before doing any other actions on Chrome.
    
    The URL should be a string. For example: https://gmail.com
    """
    p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    script = f'''
    tell application "Google Chrome"
        open location "{url}"
    end tell
    '''
    stdout, stderr = p.communicate(script.encode('utf-8'))

    if p.returncode != 0:
        raise Exception(stderr)

    return stdout

def run_javascript(javascript):
    p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
    stdout, stderr = p.communicate(script.encode('utf-8'))

    if p.returncode != 0:
        raise Exception(stderr)

    return stdout

if __name__ == '__main__':
    chrome_open_url('https://gmail.com')