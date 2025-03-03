# modules/deepseek_api.py
import requests
import json

class DeepSeekHelper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    def ask(self, prompt, mode="default"):
        # 模式定制示例
        if mode == "code":
            prompt = f"请用Python回答：{prompt}"
        elif mode == "creative":
            prompt = f"请用幽默的方式回答：{prompt}"

        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(self.base_url, headers=self.headers, json=data)
        return response.json()["choices"][0]["message"]["content"]