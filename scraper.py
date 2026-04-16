import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.freejobalert.com/"


def fetch_jobs():
    res = requests.get(BASE_URL)
    soup = BeautifulSoup(res.text, "html.parser")

    jobs = []

    for a in soup.find_all("a"):
        title = a.text.strip()
        link = a.get("href")

        if not title or not link:
            continue

        if not link.startswith("http"):
            continue

        title_lower = title.lower()

        # 🔥 STRICT FILTER
        if any(x in title_lower for x in ["recruitment", "apply", "online"]):
            category = "latest_job"

        elif "admit card" in title_lower:
            category = "admit_card"

        elif "result" in title_lower:
            category = "result"

        else:
            continue

        # ❌ remove garbage
        if len(title) < 15:
            continue

        jobs.append({
            "title": title,
            "url": link,
            "category": category,
            "apply_link": link
        })

    return jobs


def fetch_details(job):
    # CLEAN MODE → no messy parsing
    job["start_date"] = "Check Official"
    job["last_date"] = "Check Official"
    job["exam_date"] = "Check Official"

    job["fee_gen"] = "0"
    job["fee_sc"] = "0"
    job["fee_female"] = "0"

    return job
