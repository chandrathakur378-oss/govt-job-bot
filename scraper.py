import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.sarkariresult.com"


def fetch_jobs():
    res = requests.get(BASE_URL, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    jobs = []
    jobs += extract_links(soup, "Latest Jobs", "latest_job")
    jobs += extract_links(soup, "Admit Card", "admit_card")
    jobs += extract_links(soup, "Result", "result")

    return jobs


def extract_links(soup, section_name, category):
    jobs = []

    for h2 in soup.find_all("h2"):
        if section_name.lower() in h2.text.lower():

            ul = h2.find_next("ul")
            if not ul:
                continue

            for li in ul.find_all("li"):
                a = li.find("a")
                if not a:
                    continue

                title = a.text.strip()
                link = a.get("href")

                if not title or not link:
                    continue

                if link.startswith("/"):
                    link = BASE_URL + link

                # 🔥 strict filter
                if len(title) < 20:
                    continue

                if any(x in title.lower() for x in ["home", "click here"]):
                    continue

                jobs.append({
                    "title": title,
                    "url": link,
                    "category": category
                })

    return jobs


def fetch_details(job):
    try:
        res = requests.get(job["url"], timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text(" ", strip=True)

        job["start_date"] = extract(text, r"Start Date\s*[:\-]?\s*(\d{1,2}\s\w+\s\d{4})")
        job["last_date"] = extract(text, r"Last Date\s*[:\-]?\s*(\d{1,2}\s\w+\s\d{4})")
        job["exam_date"] = extract(text, r"Exam Date\s*[:\-]?\s*([0-9A-Za-z \-]+)")

        job["fee_gen"] = extract_fee(text, "General|OBC|EWS")
        job["fee_sc"] = extract_fee(text, "SC|ST")
        job["fee_female"] = extract_fee(text, "Female")

        job["apply_link"] = extract_apply_link(soup, job["category"], job["url"])

    except Exception as e:
        print("Error:", e)

    return job


def extract_apply_link(soup, category, fallback):
    for a in soup.find_all("a"):
        text = a.text.lower()
        href = a.get("href", "")

        if not href.startswith("http"):
            continue

        if any(x in href for x in ["play.google", "facebook", "youtube"]):
            continue

        if category == "latest_job":
            if "apply" in text or "registration" in text:
                return href

        elif category == "admit_card":
            if "admit" in text or "download" in text:
                return href

        elif category == "result":
            if "result" in text or "check" in text:
                return href

    return fallback


def extract(text, pattern):
    m = re.search(pattern, text, re.IGNORECASE)
    return m.group(1) if m else "N/A"


def extract_fee(text, keyword):
    m = re.search(rf"({keyword})[^₹0-9]*₹?\s*(\d+)", text, re.IGNORECASE)
    return m.group(2) if m else "0"
