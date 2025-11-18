import requests
import config

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


def send_message(text: str, token: str = None, chat_id: str = None) -> bool:
    token = token or config.TELEGRAM_TOKEN
    chat_id = chat_id or config.CHAT_ID
    try:
        resp = requests.post(
            TELEGRAM_API.format(token=token),
            json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        )
        resp.raise_for_status()
        return resp.ok
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False
