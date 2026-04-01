# ChatBot Auto-Reply (Python + React)

## Structure
- `bot.py`: bot engine + OpenAI integration
- `server.py`: Flask API for start/stop/status
- `frontend/`: React UI (Vite)

## Setup
1. `pip install pyautogui pyperclip openai flask`
2. Set API key:
   - `setx OPENAI_API_KEY "your_key"` (Windows) OR
   - `export OPENAI_API_KEY=your_key` (macOS/Linux) OR set explicit in `bot.py`

3. Run backend:
   - `python server.py`

4. Run front-end:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

5. Open `http://localhost:5173`

## Notes
- Ensure correct screen coordinates in `bot.py`.
- For safety, move mouse to top-left corner to trigger PyAutoGUI failsafe.
