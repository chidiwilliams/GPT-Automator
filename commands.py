import subprocess

from langchain.agents import tool

@tool
def computer_action(apple_script):
    """
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

    Write the AppleScript for the Command:
    """
    p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(apple_script.encode('utf-8'))

    if p.returncode != 0:
        raise Exception(stderr)

    return stdout

def chrome_action(javascript):
    p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    script = f'''
    tell application "Google Chrome"
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