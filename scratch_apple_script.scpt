tell application "Google Chrome"
    tell active tab of front window
        execute javascript "window.alert('hello')"
    end tell
end tell