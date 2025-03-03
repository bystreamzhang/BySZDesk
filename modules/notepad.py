# modules/notepad.py
from datetime import datetime
import os

class NoteManager:
    def __init__(self, notes_dir="notes"):
        self.notes_dir = notes_dir
        os.makedirs(notes_dir, exist_ok=True)

    @property
    def today_file(self):
        return f"{self.notes_dir}/{datetime.now().strftime('%Y-%m-%d')}.txt"

    def save_note(self, text):
        with open(self.today_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%H:%M')}]\n{text}\n\n")

    def load_notes(self, date_str):
        file_path = f"{self.notes_dir}/{date_str}.txt"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        return "暂无记录"