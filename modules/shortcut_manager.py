# modules/shortcut_manager.py
import json
import os
import subprocess

class ShortcutManager:
    def __init__(self, config_file="shortcuts.json"):
        self.config_file = config_file
        self.shortcuts = self._load_shortcuts()

    def _load_shortcuts(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f)
        return {}

    def add_shortcut(self, name, path):
        self.shortcuts[name] = path
        self._save()

    def _save(self):
        with open(self.config_file, "w") as f:
            json.dump(self.shortcuts, f)

    def open_shortcut(self, name):
        path = self.shortcuts.get(name)
        if path and os.path.exists(path):
            subprocess.Popen(f'explorer "{path}"', shell=True)