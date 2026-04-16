import requests
import time
import random

from scraper import fetch_jobs
from classifier import classify_job
from formatter import format_message
from dedupe import load_seen, save_seen, is_new, mark_seen
from config import BOT_TOKEN, CHANNEL_ID, ADMIN_ID, CHECK_INTERVAL, MAX_POSTS
from controller import get_status, set_status

# Load seen jobs
seen = load_seen()

# Telegram send function
def send_telegram(text, chat_id=CHANNEL_ID):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print("Telegram Error:", e)


# Smart delay
def get_delay(category):
    if category == "result":
        return random.randint(120, 240)

    elif category == "admit_card":
        return random.randint(180, 300)

    elif category == "latest_job":
        return random.randint(300, 600)

    return random.randint(180, 300)


# ================= TELEGRAM CONTROL =================

update_id = None

def get_updates():
    global update_id

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

    params = {
        "timeout": 10,
        "offset": update_id
    }

    try:
        res = requests.get(url, params=params, timeout=10).json()

        for item in res.get("result", []):
            update_id = item["update_id"] + 1

            if "message" in item:
                text = item["message"].get("text", "")
                user_id = str(item["message"]["from"]["id"])

                handle_command(text, user_id)

    except Exception as e:
        print("Update Error:", e)


def handle_command(text, user_id):
    if str(user_id) != str(ADMIN_ID):
        return

    text = text.lower()

    if text == "/startbot":
        set_status("running")
        send_telegram("▶️ Bot Started", ADMIN_ID)

    elif text == "/pausebot":
        set_status("paused")
        send_telegram("⏸ Bot Paused", ADMIN_ID)

    elif text == "/stopbot":
        set_status("stopped")
        send_telegram("🛑 Bot Stopped", ADMIN_ID)

    elif text == "/status":
        status = get_status()
        send_telegram(f"📊 Status: {status}", ADMIN_ID)

    elif text == "/help":
        send_telegram("""📌 Commands:
/startbot - Start
/pausebot - Pause
/stopbot - Stop
/status - Status
""", ADMIN_ID)


# ================= MAIN LOOP =================

while True:
    try:
        # 🔹 Listen for Telegram commands
        get_updates()

        status = get_status()

        if status == "paused":
            print("⏸ Bot Paused")
            time.sleep(5)
            continue

        if status == "stopped":
            print("🛑 Bot Stopped")
            break

        print("🔍 Checking for new jobs...")

        jobs = fetch_jobs()
        count = 0

        for job in jobs:
            if count >= MAX_POSTS:
                break

            if not is_new(job, seen):
                continue

            category = classify_job(job)
            msg = format_message(job, category)

            print(f"🚀 Posting: {job['title']}")

            send_telegram(msg)

            mark_seen(job, seen)
            save_seen(seen)

            delay = get_delay(category)
            print(f"⏳ Waiting {delay} sec")
            time.sleep(delay)

            count += 1

        print(f"😴 Sleeping {CHECK_INTERVAL} sec\n")
        time.sleep(CHECK_INTERVAL)

    except Exception as e:
        print("❌ Error:", e)
        time.sleep(30)