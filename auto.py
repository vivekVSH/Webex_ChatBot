import os
import time
import pyautogui
import pyperclip
from openai import OpenAI

# Set OPENAI_API_KEY environment variable, or uncomment and set directly:
# client = OpenAI(api_key="YOUR_OPENAI_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise RuntimeError("OPENAI_API_KEY is not set. Use environment variable or assign directly in auto.py")
client = OpenAI(api_key=openai_api_key)

# Replace these with the coordinates you captured
SCAN_START = (573, 13318)
SCAN_END = (574, 10098)
CLICK_SEND = (1834, 9883)

LOOP_DELAY = 3.0

pyautogui.FAILSAFE = True

def read_chat_text():
    pyautogui.moveTo(*SCAN_START, duration=0.2)
    pyautogui.mouseDown()
    pyautogui.moveTo(*SCAN_END, duration=0.25)
    pyautogui.mouseUp()
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.2)
    return pyperclip.paste().strip()


def generate_reply(message_text: str) -> str:
    if not message_text:
        return ""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a friendly, concise chat assistant."},
            {"role": "user", "content": message_text},
        ],
        temperature=0.7,
        max_tokens=180,
    )
    return resp.choices[0].message.content.strip()


def send_reply(reply_text: str):
    if not reply_text:
        return
    pyautogui.click(*CLICK_SEND)
    time.sleep(0.2)
    pyperclip.copy(reply_text)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.2)
    pyautogui.press("enter")


def main():
    print("Auto-reply running. Press Ctrl+C to stop.")
    last_text = ""
    while True:
        try:
            text = read_chat_text()
            if text and text != last_text:
                print("New text detected. Generating reply...")
                reply = generate_reply(text)
                if reply:
                    print("Reply sent:", reply[:80].replace("\n", " "))
                    send_reply(reply)
                    last_text = text
                else:
                    print("No reply generated")
            else:
                print("No new text (or empty).")
            time.sleep(LOOP_DELAY)
        except KeyboardInterrupt:
            print("\nStopped by user")
            break


if __name__ == "__main__":
    main()