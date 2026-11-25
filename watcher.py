import os, re, json, smtplib, requests
from email.message import EmailMessage

URL = "https://www.dasweltauto.at/vehicle/15005515"
STATE = "state.json"
USER, PASS = os.environ["SMTP_USER"], os.environ["SMTP_PASS"]
TO = os.environ.get("MAIL_TO", USER)

r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
r.raise_for_status()
ids = sorted(set(re.findall(r"/images/([0-9a-f]{8}-[0-9a-f-]{27})", r.text)))
print("images:", len(ids), "| placeholder:", "Bilder folgen in Kürze" in r.text)

try:
    base = json.load(open(STATE))["ids"]
except Exception:
    base = None

if base is not None and ids != base:
    msg = EmailMessage()
    msg["Subject"] = "Caddy: photos are online!"
    msg["From"], msg["To"] = USER, TO
    msg.set_content(f"New pictures appeared:\n{URL}")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(USER, PASS)
        s.send_message(msg)
    print("Email sent")

json.dump({"ids": ids}, open(STATE, "w"))