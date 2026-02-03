import requests
import hashlib
import os
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

URL = "https://entradas.7yaccion.com/o/2/el-hormiguero"
HASH_FILE = "last_hash.txt"

EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = "mesbb60@gmail.com"
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

def get_page_hash():
    r = requests.get(URL, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    # Limpiamos cosas volátiles
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

def send_email():
    msg = MIMEText(
        f"La web ha cambiado:\n\n{URL}",
        "plain",
        "utf-8"
    )
    msg["Subject"] = "🚨 Cambio detectado en El Hormiguero"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

def main():
    current_hash = get_page_hash()
    last_hash = load_last_hash()

    if last_hash and current_hash != last_hash:
        print("Cambio detectado, enviando email")
        send_email()
    else:
        print("Sin cambios")

    save_hash(current_hash)

if __name__ == "__main__":
    main()
