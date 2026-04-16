def clean(value):
    if not value or value == "N/A":
        return "N/A"
    return value


def format_message(job, category):
    title = job.get("title", "N/A")

    # 🔥 Use real apply link
    link = job.get("apply_link", job.get("url", "#"))

    start_date = clean(job.get("start_date"))
    last_date = clean(job.get("last_date"))
    exam_date = clean(job.get("exam_date"))

    fee_gen = clean(job.get("fee_gen"))
    fee_sc = clean(job.get("fee_sc"))
    fee_female = clean(job.get("fee_female"))

    # ================= JOB =================
    if category == "latest_job":
        return f"""
🔥 GOVT JOB ALERT

━━━━━━━━━━━━━━━━━━
🆕 {title}

📅 Start Date: {start_date}
⏳ Last Date: {last_date}

💰 Application Fee:
▫️ General / OBC / EWS: ₹{fee_gen}
▫️ SC / ST: ₹{fee_sc}
▫️ Female: ₹{fee_female}

📅 Exam Date: {exam_date}

━━━━━━━━━━━━━━━━━━
🚀 APPLY ONLINE 👇
<a href="{link}">Click Here</a>
"""

    # ================= ADMIT CARD =================
    elif category == "admit_card":
        return f"""
🎫 ADMIT CARD RELEASED

━━━━━━━━━━━━━━━━━━
🔥 {title}

📅 Exam Date: {exam_date}

━━━━━━━━━━━━━━━━━━
📥 DOWNLOAD ADMIT CARD 👇
<a href="{link}">Click Here</a>
"""

    # ================= RESULT =================
    elif category == "result":
        return f"""
📊 RESULT DECLARED

━━━━━━━━━━━━━━━━━━
⚡ {title}

🎯 Check Your Result Now
⏳ High Traffic Expected

━━━━━━━━━━━━━━━━━━
📎 CHECK RESULT 👇
<a href="{link}">Click Here</a>
"""

    # ================= FALLBACK =================
    return f"""
📢 UPDATE

━━━━━━━━━━━━━━━━━━
{title}

━━━━━━━━━━━━━━━━━━
🔗 <a href="{link}">Click Here</a>
"""
