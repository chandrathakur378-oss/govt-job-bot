import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.sarkariresult.com"


# ================= FETCH ALL JOB LINKS =================

def fetch_jobs():
    url = BASE_URL + "/"
    res = requests.get(url, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    jobs = []

    jobs += extract_links(soup, "Latest Jobs", "latest_job")
    jobs += extract_links(soup, "Admit Card", "admit_card")
    jobs += extract_links(soup, "Result", "result")

    return jobs


# ================= EXTRACT LINKS =================

def extract_links(soup, section, category):
    jobs = []

    for div in soup.find_all("div"):
        if section.lower() in div.text.lower():

            ul = div.find_next("ul")
            if not ul:
                continue

            for li in ul.find_all("li"):
                a = li.find("a")
                if not a:
                    continue

                title = a.text.strip()
                link = a.get("href")

                if not link or len(title) < 10:
                    continue

                if link.startswith("/"):
                    link = BASE_URL + link

                if BASE_URL not in link:
                    continue

                jobs.append({
                    "title": title,
                    "url": link,
                    "category": category
                })

    return jobs


# ================= FETCH FULL DETAILS =================

def fetch_details(job):
    try:
        res = requests.get(job["url"], timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        text = soup.get_text(" ", strip=True)

        job["start_date"] = extract(text, r"Start Date\s*[:\-]?\s*([0-9A-Za-z ]+)")
        job["last_date"] = extract(text, r"Last Date\s*[:\-]?\s*([0-9A-Za-z ]+)")
        job["exam_date"] = extract(text, r"Exam Date\s*[:\-]?\s*([0-9A-Za-z \-]+)")

        job["fee_gen"] = extract(text, r"(General|OBC|EWS)[^0-9]*([0-9]+)")
        job["fee_sc"] = extract(text, r"(SC|ST)[^0-9]*([0-9]+)")
        job["fee_female"] = extract(text, r"(Female)[^0-9]*([0-9]+)")

    except:
        pass

    return job


# ================= REGEX HELPER =================

def extract(text, pattern):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "N/A"
