def format_message(job, category):
    title = job["title"]
    link = job["apply_link"]

    if category == "latest_job":
        return f"""
🔥 GOVT JOB ALERT

━━━━━━━━━━━━━━━━━━
🆕 {title}

📌 Full details available below

━━━━━━━━━━━━━━━━━━
🚀 APPLY ONLINE 👇
<a href="{link}">Click Here</a>
"""

    elif category == "admit_card":
        return f"""
🎫 ADMIT CARD RELEASED

━━━━━━━━━━━━━━━━━━
🔥 {title}

━━━━━━━━━━━━━━━━━━
📥 DOWNLOAD ADMIT CARD 👇
<a href="{link}">Click Here</a>
"""

    elif category == "result":
        return f"""
📊 RESULT DECLARED

━━━━━━━━━━━━━━━━━━
⚡ {title}

━━━━━━━━━━━━━━━━━━
📎 CHECK RESULT 👇
<a href="{link}">Click Here</a>
"""
