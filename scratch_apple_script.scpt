# tell application "Google Chrome"
# 	activate
# 	open location "https://google.com"
# end tell

# property javascriptSnippet = "window.location.href = 'https://google.com';"
# property javascriptSnippet = "document.querySelectorAll(\"button\");"

# tell application "Google Chrome"
#     tell active tab of front window
#         execute javascript javascriptSnippet
#     end tell
# end tell

tell application "Notion"
    activate
    delay 0.5
    tell application "System Events" to keystroke "p" using {command down}
    delay 1
    keystroke "H"
    keystroke return
end tell