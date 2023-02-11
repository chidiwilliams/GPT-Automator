import subprocess

from langchain.agents import tool

@tool
def computer_action(apple_script):
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

    p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(apple_script.encode('utf-8'))

    if p.returncode != 0:
        raise Exception(stderr)

    return stdout

@tool
def chrome_action(javascript):
    """
    Use this when you want to execute a command on Chrome. The command should be in Javascript.

    Here are some examples of good Javascript commands:

    Command: Get the links on the page
    document.querySelectorAll('a').forEach(a => console.log(a.href))

    Command: Get the buttons on the page
    document.querySelectorAll('button').forEach(a => console.log(a.innerText))

    Write the Javascript for the command:
    """
    p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    script = f'''
    tell application "Google Chrome"
        activate
        execute javascript "{javascript}" in active tab of window 1
    end tell
    '''
    stdout, stderr = p.communicate(script.encode('utf-8'))

    if p.returncode != 0:
        raise Exception(stderr)

    return stdout

def chrome_open_url(url):
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

if __name__ == '__main__':
    chrome_open_url('https://gmail.com')