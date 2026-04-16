import requests
import time
import random
import threading

from flask import Flask

from scraper import fetch_jobs, fetch_details
from formatter import format_message
from dedupe import load_seen, save_seen, is_new, mark_seen
from controller import get_status, set_status
from config import BOT_TOKEN, CHANNEL_ID, ADMIN_ID, CHECK_INTERVAL, MAX_POSTS


# ================= FLASK =================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running ✅"


def run_flask():
    app.run(host="0.0.0.0", port=10000)


# ================= TELEGRAM =================

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    requests.post(url, data=data)


# ================= DELAY =================

def get_delay(category):
    if category == "result":
        return random.randint(120, 240)
    elif category == "admit_card":
        return random.randint(180, 300)
    else:
        return random.randint(300, 600)


# ================= MAIN LOOP =================

def run_bot():
    print("🚀 Bot Started...")

    seen = load_seen()

    while True:
        try:
            status = get_status()

            if status == "paused":
                time.sleep(5)
                continue

            if status == "stopped":
                break

            jobs = fetch_jobs()

            count = 0

            for job in jobs:

                if count >= MAX_POSTS:
                    break

                if not is_new(job, seen):
                    continue

                # 🔥 get full details
                job = fetch_details(job)

                category = job["category"]  # IMPORTANT FIX

                msg = format_message(job, category)

                print("Posting:", job["title"])

                send_telegram(msg)

                mark_seen(job, seen)
                save_seen(seen)

                time.sleep(get_delay(category))

                count += 1

            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print("Error:", e)
            time.sleep(30)


# ================= START =================

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    run_flask()
