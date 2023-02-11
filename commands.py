import subprocess

from langchain.agents import tool


@tool
def computer_action(apple_script):
    """
    Use this when you want to execute a command on the computer. The command should be in AppleScript.
    Here are some examples of good AppleScript commands:

    Command: Search for a table nearby
    AppleScript: tell application "Google Chrome"
    activate
    open location "https://www.google.com/search?q=Table+nearby"
    end tell

    The AppleScript should be valid and never use keyboard shortcuts.
    Write the AppleScript for the Command:
    """
    p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f'sending to terminal:\n{apple_script}')
    stdout, stderr = p.communicate(apple_script.encode('utf-8'))

    if p.returncode != 0:
        raise Exception(stderr)

    return stdout


@tool
def get_url_compose_gmail(url_extension):
    """
    Use this when you want to create a url extension to send an email with gmail.
    Here are some examples of good url extensions:

    Command: Write an email to john@example.com
    url_extension: to=john@example.com

    Command: Write an email to adam@gmail.com
    url_extension: to=adam@gmail.com

    Command: Write an email to jess@house.com
    url_extension: to=jess@house.com
    
    The URL should be valid and never use keyboard shortcuts.
    Write the url_extension for the Command:
    """

    initial_url = 'https://mail.google.com/mail/?view=cm&fs=1&'
    url = initial_url + url_extension
    return url




@tool
def chrome_open_url(url):
    """
    Use this when you want to get a specific URL with Chrome. The command should be in AppleScript.

    Here are some examples of good AppleScript commands:

    Command: Search for a table nearby
    AppleScript: tell application "Google Chrome"
    activate
    open location "https://www.google.com/search?q=Table+nearby"
    end tell

    The AppleScript should be valid and never appropriate use keyboard shortcuts.

    Write the AppleScript for the Command:
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


@tool
def chrome_action(javascript):
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
    p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    script = f'''
    tell application "Google Chrome"
        activate
            tell active tab of front window
            execute javascript "{javascript}" in active tab of window 1
        end tell
    end tell
    '''
    stdout, stderr = p.communicate(script.encode('utf-8'))

    if p.returncode != 0:
        raise Exception(stderr)

    return stdout

