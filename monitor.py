import requests
import hashlib
import os
from bs4 import BeautifulSoup

URL = "https://entradas.7yaccion.com/o/2/el-hormiguero"

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def get_page_hash():
    r = requests.get(URL, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def load_last_hash():
    if not os.path.exists(HASH_FILE):
        return None
    with open(HASH_FILE, "r") as f:
        return f.read().strip()

def save_hash(h):
    with open(HASH_FILE, "w") as f:
        f.write(h)

def send_telegram():
    msg = (
        "🚨 *Cambio detectado en El Hormiguero*\n\n"
        f"{URL}"
    )

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        },
        timeout=10
    )

def main():
    current_hash = get_page_hash()
    last_hash = load_last_hash()
    

    if last_hash and current_hash != last_hash:
        print("Cambio detectado → Telegram")
        send_telegram()
    else:
        print("Sin cambios")

    save_hash(current_hash)

if __name__ == "__main__":
    main()
