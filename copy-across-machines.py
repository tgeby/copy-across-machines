import time
import pyperclip

last_clipboard_content = ""

while True:
    time.sleep(1)  # Check every second
    clipboard_content = pyperclip.paste()
    if clipboard_content != last_clipboard_content:
        print("Clipboard updated:", clipboard_content)
        last_clipboard_content = clipboard_content
    