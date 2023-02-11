import subprocess

from langchain.agents import tool

@tool
def chrome_os_action(apple_script):
    """
    Use this when you want to control the computer. The command should be in AppleScript.

    It is good for opening Chrome and interacting with other apps, but not for interacting with the Chrome itself.

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
    print("Running AppleScript: ", apple_script)
    p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(apple_script.encode('utf-8'))

    if p.returncode != 0:
        raise Exception(stderr)

    return stdout

@tool
def chrome_javascript_action(javascript):
    """
    Use this when you want to execute a command in Chrome. The command should be Javascript.

    You can also use the javascript commands to learn more about the page you're on.

    Here are some helpful Javascript commands:

    Command: Get the clickable elements on the page
    Javascript: Array.from(document.querySelectorAll('a, button, input[type="submit"], input[type="button"]'))

    Command: Click the button with the text "Sign in"
    Javascript: document.querySelector('button:contains("Sign in")').click()

    Command: Enter the text "Hello" into the input with the placeholder "Search"
    Javascript: document.querySelector('input[placeholder="Search"]').value = "Hello"

    The Javascript must be valid including quotes and semicolons.

    Write the Javascript for the Command:
    """
    print("Running Javascript: ", javascript)

    p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    script = f'''
    tell application "Google Chrome"
        activate
        tell active tab of front window
            execute javascript "{javascript}"
        end tell
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