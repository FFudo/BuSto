import requests

from config import DISCORD_URL


class DiscordWebhook:
    def __init__(self):
        self.url = DISCORD_URL
        self.username = "BuSto"
        self.avatar_url = "https://img.freepik.com/free-vector/ai-technology-robot-cyborg-design_24640-134415.jpg?t=st=1739204923~exp=1739208523~hmac=8c4abe816afb26747d5cbc9169a4a360e54d39bc52cd17d9064f4ef9e3225e1e&w=1380"

    def send_message(self, message: str):
        message = {
            "username": self.username,
            "avatar_url": self.avatar_url,
            "content": message,
        }
        response = requests.post(self.url, json=message)
        response.raise_for_status()
