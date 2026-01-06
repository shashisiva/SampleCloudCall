# call_moderation_api.py
import requests

API_URL = "http://127.0.0.1:8000/moderate"

text_to_check = "You are stupid"

resp = requests.post(API_URL, json={"text": text_to_check}, timeout=30)
resp.raise_for_status()  # raises error if API returns 4xx/5xx

print(resp.json())
