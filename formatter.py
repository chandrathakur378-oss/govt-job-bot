def format_message(job, category):

    title = job.get("title", "N/A")
    link = job.get("url", "#")

    if category == "latest_job":
        return f"""
🔥 GOVT JOB ALERT

━━━━━━━━━━━━━━━━━━
🆕 {title}

📅 Start Date: {job.get('start_date', 'N/A')}
⏳ Last Date: {job.get('last_date', 'N/A')}

💰 Application Fee:
▫️ General / OBC / EWS: ₹{job.get('fee_gen', 'N/A')}
▫️ SC / ST: ₹{job.get('fee_sc', 'N/A')}
▫️ Female: ₹{job.get('fee_female', 'N/A')}

📅 Exam Date: {job.get('exam_date', 'N/A')}

━━━━━━━━━━━━━━━━━━
🚀 APPLY ONLINE 👇
<a href="{link}">Click Here</a>
"""

    elif category == "admit_card":
        return f"""
🎫 ADMIT CARD RELEASED

━━━━━━━━━━━━━━━━━━
🔥 {title}

📅 Exam Date: {job.get('exam_date', 'N/A')}

━━━━━━━━━━━━━━━━━━
📥 DOWNLOAD ADMIT CARD 👇
<a href="{link}">Click Here</a>
"""

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
