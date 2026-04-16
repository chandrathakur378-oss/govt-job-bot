import requests
import time
import random
import threading

from flask import Flask

from scraper import fetch_jobs, fetch_details
from formatter import format_message
from dedupe import load_seen, save_seen, is_new, mark_seen
from controller import get_status
from config import BOT_TOKEN, CHANNEL_ID, CHECK_INTERVAL, MAX_POSTS


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

    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print("❌ Telegram Error:", e)


# ================= DELAY =================

def get_delay(category):
    if category == "result":
        return random.randint(120, 240)
    elif category == "admit_card":
        return random.randint(180, 300)
    else:
        return random.randint(300, 600)


# ================= BOT LOOP =================

def run_bot():
    print("🚀 Bot Started...")   # 🔥 IMPORTANT DEBUG

    seen = load_seen()

    while True:
        try:
            print("🔍 Fetching jobs...")  # 🔥 DEBUG

            status = get_status()

            if status == "paused":
                print("⏸ Paused")
                time.sleep(5)
                continue

            if status == "stopped":
                print("🛑 Stopped")
                break

            jobs = fetch_jobs()

            print(f"📊 Found {len(jobs)} jobs")  # DEBUG

            count = 0

            for job in jobs:

                if count >= MAX_POSTS:
                    break

                if not is_new(job, seen):
                    continue

                # 🔥 Get full details
                job = fetch_details(job)

                category = job["category"]

                msg = format_message(job, category)

                print(f"📤 Posting: {job['title']}")

                send_telegram(msg)

                mark_seen(job, seen)
                save_seen(seen)

                delay = get_delay(category)
                print(f"⏳ Delay: {delay}s")

                time.sleep(delay)

                count += 1

            print(f"😴 Sleeping {CHECK_INTERVAL}s...\n")
            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print("❌ ERROR:", e)
            time.sleep(10)


# ================= START =================

if __name__ == "__main__":
    try:
        print("🔥 Starting system...")

        # 🔥 START BOT THREAD (FIXED)
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.daemon = True   # VERY IMPORTANT
        bot_thread.start()

        print("🌐 Starting Flask server...")

        # 🔥 START FLASK
        run_flask()

    except Exception as e:
        print("❌ MAIN ERROR:", e)
