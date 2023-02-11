import subprocess


def action(apple_script):
    p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(script.encode('utf-8'))

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