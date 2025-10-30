import requests
from ..config import Config

def send_push(tokens, title, body, data=None):
    key = Config().FCM_SERVER_KEY
    if not key:
        return False, "FCM_SERVER_KEY not configured"
    r = requests.post(
        "https://fcm.googleapis.com/fcm/send",
        json={"registration_ids": tokens, "notification": {"title": title, "body": body}, "data": data or {}},
        headers={"Authorization": f"key={key}", "Content-Type": "application/json"},
        timeout=10
    )
    return (r.status_code == 200, (r.json() if r.status_code == 200 else r.text))
