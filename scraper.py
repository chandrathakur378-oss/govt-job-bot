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

    for div in soup.find_all("div"):
        if section_name.lower() in div.text.lower():

            ul = div.find_next("ul")
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

                # ❌ skip bad titles
                if len(title) < 15:
                    continue

                if "latest jobs" in title.lower():
                    continue

                if BASE_URL not in link:
                    continue

                jobs.append({
                    "title": title,
                    "url": link,
                    "category": category
                })

    return jobs


# ================= DETAILS =================

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

        job["apply_link"] = extract_apply_link(soup, job["url"])

    except Exception as e:
        print("Error:", e)

    return job


# ================= APPLY LINK =================

def extract_apply_link(soup, fallback):
    for a in soup.find_all("a"):
        if "apply online" in a.text.lower():
            return a.get("href")

    for a in soup.find_all("a"):
        if "registration" in a.text.lower():
            return a.get("href")

    for a in soup.find_all("a"):
        href = a.get("href", "")
        if href.startswith("http") and "sarkariresult" not in href:
            return href

    return fallback


# ================= HELPERS =================

def extract(text, pattern):
    m = re.search(pattern, text, re.IGNORECASE)
    return m.group(1) if m else "N/A"


def extract_fee(text, keyword):
    pattern = rf"({keyword})[^0-9₹]*₹?\s*([0-9]+)"
    m = re.search(pattern, text, re.IGNORECASE)
    return m.group(2) if m else "0"
