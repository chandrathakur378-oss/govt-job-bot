import requests
import time
import random
import threading

from flask import Flask

from scraper import fetch_jobs, fetch_details
from formatter import format_message
from dedupe import load_seen, save_seen, is_new, mark_seen
from config import BOT_TOKEN, CHANNEL_ID, CHECK_INTERVAL, MAX_POSTS


app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running ✅"


def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    requests.post(url, data=data)


def get_delay():
    return random.randint(180, 300)


def run_bot():
    print("🚀 Clean Bot Started...")

    seen = load_seen()

    while True:
        try:
            print("🔍 Fetching clean jobs...")

            jobs = fetch_jobs()
            count = 0

            for job in jobs:

                if count >= MAX_POSTS:
                    break

                if not is_new(job, seen):
                    continue

                job = fetch_details(job)

                msg = format_message(job, job["category"])

                print("📤 Posting:", job["title"])

                send_telegram(msg)

                mark_seen(job, seen)
                save_seen(seen)

                time.sleep(get_delay())
                count += 1

            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print("Error:", e)
            time.sleep(10)


if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.daemon = True
    t.start()

    app.run(host="0.0.0.0", port=10000)
