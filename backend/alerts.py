
import os,requests
def send_alert(msg):
    token=os.environ.get("TELEGRAM_TOKEN")
    chat=os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat: return
    try:
        requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id":chat,"text":msg},
        timeout=10)
    except: pass
