import time
import threading
import pyautogui
import pyperclip
from openai import OpenAI

# Set OPENAI_API_KEY in environment or here:
# client = OpenAI(api_key="YOUR_OPENAI_API_KEY")
client = OpenAI()

SCAN_START = (573, 13318)
SCAN_END = (574, 10098)
CLICK_SEND = (1834, 9883)
LOOP_DELAY = 3.0
pyautogui.FAILSAFE = True

class AutoReplyBot:
    def __init__(self):
        self._running = False
        self._thread = None
        self.last_text = ""
        self.status = "Stopped"

    def _read_chat_text(self):
        pyautogui.moveTo(*SCAN_START, duration=0.2)
        pyautogui.mouseDown()
        pyautogui.moveTo(*SCAN_END, duration=0.25)
        pyautogui.mouseUp()
        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.2)
        return pyperclip.paste().strip()

    def _generate_reply(self, message_text: str) -> str:
        if not message_text:
            return ""
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful, concise assistant."},
                {"role": "user", "content": message_text},
            ],
            temperature=0.7,
            max_tokens=180,
        )
        return resp.choices[0].message.content.strip()

    def _send_reply(self, reply_text: str):
        if not reply_text:
            return
        pyautogui.click(*CLICK_SEND)
        time.sleep(0.2)
        pyperclip.copy(reply_text)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.2)
        pyautogui.press("enter")

    def _run_loop(self):
        self.status = "Running"
        while self._running:
            try:
                text = self._read_chat_text()
                if text and text != self.last_text:
                    self.status = "Processing"
                    reply = self._generate_reply(text)
                    self._send_reply(reply)
                    self.last_text = text
                    self.status = "Waiting"
                else:
                    self.status = "Waiting"
                time.sleep(LOOP_DELAY)
            except Exception as ex:
                self.status = f"Error: {ex}"
                self._running = False
                break

        self.status = "Stopped"

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=5)
        self.status = "Stopped"

    def get_status(self):
        return self.status

if __name__ == "__main__":
    bot = AutoReplyBot()
    bot.start()
    try:
        while True:
            print(bot.get_status())
            time.sleep(2)
    except KeyboardInterrupt:
        bot.stop()
