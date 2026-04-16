def format_message(job, category):
    link = f'<a href="{job["url"]}">Click Here</a>'

    if category == "latest_job":
        return f"""
🔥 GOVT JOB ALERT

━━━━━━━━━━━━━━━━━━
{job['title']} 🆕

━━━━━━━━━━━━━━━━━━
📝 APPLY ONLINE 👉 {link}
"""

    elif category == "admit_card":
        return f"""
🎫 ADMIT CARD RELEASED

━━━━━━━━━━━━━━━━━━
{job['title']} 🔥 OUT

━━━━━━━━━━━━━━━━━━
📥 DOWNLOAD ADMIT CARD 👉 {link}
"""

    elif category == "result":
        return f"""
📊 RESULT DECLARED

━━━━━━━━━━━━━━━━━━
{job['title']} ⚡ LIVE

━━━━━━━━━━━━━━━━━━
📎 CHECK RESULT 👉 {link}
"""