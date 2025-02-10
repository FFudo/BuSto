import requests

from config import DISCORD_URL


class DiscordWebhook:
    def __init__(self):
        self.url = DISCORD_URL
        self.username = "BuSto"
        self.avatar_url = "https://img.freepik.com/free-vector/cute-robot-wearing-hat-flying-cartoon-vector-icon-illustration-science-technology-icon-isolated_138676-5186.jpg?t=st=1739218240~exp=1739221840~hmac=f48675c8a40c88148b55e38d7fd9fb3ae3de3bfbaf27b233ef551bdc08fab7c7&w=1380"

    def send_message(self, message: str):
        message = {
            "username": self.username,
            "avatar_url": self.avatar_url,
            "content": message,
        }
        response = requests.post(self.url, json=message)
        response.raise_for_status()
