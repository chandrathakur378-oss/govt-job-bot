def clean(v):
    return v if v and v != "N/A" else "N/A"


def format_message(job, category):
    title = job.get("title", "N/A")
    link = job.get("apply_link", job.get("url"))

    start = clean(job.get("start_date"))
    last = clean(job.get("last_date"))
    exam = clean(job.get("exam_date"))

    fee_gen = job.get("fee_gen", "0")
    fee_sc = job.get("fee_sc", "0")
    fee_female = job.get("fee_female", "0")

    if category == "latest_job":
        return f"""
🔥 GOVT JOB ALERT

━━━━━━━━━━━━━━━━━━
🆕 {title}

📅 Start Date: {start}
⏳ Last Date: {last}

💰 Application Fee:
▫️ General / OBC / EWS: ₹{fee_gen}
▫️ SC / ST: ₹{fee_sc}
▫️ Female: ₹{fee_female}

📅 Exam Date: {exam}

━━━━━━━━━━━━━━━━━━
🚀 APPLY ONLINE 👇
<a href="{link}">Click Here</a>
"""

    elif category == "admit_card":
        return f"""
🎫 ADMIT CARD RELEASED

━━━━━━━━━━━━━━━━━━
🔥 {title}

📅 Exam Date: {exam}

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
