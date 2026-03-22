import os
import requests


def send_telegram(text: str) -> tuple[bool, str]:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        return False, "missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        r = requests.post(url, json=payload, timeout=8)
        if r.ok:
            return True, "ok"
        return False, f"http {r.status_code}: {r.text[:200]}"
    except Exception as e:
        return False, str(e)
