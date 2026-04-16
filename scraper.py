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


# ================= EXTRACT LINKS FROM SECTIONS =================

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

                # ❌ Skip invalid
                if not title or not link:
                    continue

                # Fix relative URL
                if link.startswith("/"):
                    link = BASE_URL + link

                # ❌ Skip homepage
                if link.rstrip("/") == BASE_URL:
                    continue

                # ❌ Skip short/garbage titles
                if len(title) < 12:
                    continue

                # ❌ Only allow SarkariResult links
                if BASE_URL not in link:
                    continue

                # 🔥 Keyword filter (IMPORTANT)
                keywords = ["apply", "recruitment", "vacancy", "form", "admit", "result"]
                if not any(k in title.lower() for k in keywords):
                    continue

                jobs.append({
                    "title": title,
                    "url": link,
                    "category": category
                })

    return jobs


# ================= FETCH FULL JOB DETAILS =================

def fetch_details(job):
    try:
        res = requests.get(job["url"], timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        text = soup.get_text(" ", strip=True)

        # ================= DATES =================
        job["start_date"] = extract(text, r"Start Date\s*[:\-]?\s*([0-9A-Za-z ]+)")
        job["last_date"] = extract(text, r"Last Date\s*[:\-]?\s*([0-9A-Za-z ]+)")
        job["exam_date"] = extract(text, r"Exam Date\s*[:\-]?\s*([0-9A-Za-z \-]+)")

        # ================= FEES =================
        job["fee_gen"] = extract_number(text, r"(General|OBC|EWS)[^0-9]*([0-9]+)")
        job["fee_sc"] = extract_number(text, r"(SC|ST)[^0-9]*([0-9]+)")
        job["fee_female"] = extract_number(text, r"(Female)[^0-9]*([0-9]+)")

        # ================= 🔥 APPLY LINK =================
        job["apply_link"] = extract_apply_link(soup, job["url"])

    except Exception as e:
        print("❌ Detail Error:", e)

    return job


# ================= APPLY LINK LOGIC =================

def extract_apply_link(soup, fallback):
    apply_link = None

    # 🔥 Priority 1: "Apply Online"
    for a in soup.find_all("a"):
        text = a.text.lower()
        if "apply online" in text:
            apply_link = a.get("href")
            break

    # 🔥 Priority 2: "Registration"
    if not apply_link:
        for a in soup.find_all("a"):
            text = a.text.lower()
            if "registration" in text:
                apply_link = a.get("href")
                break

    # 🔥 Priority 3: external official link
    if not apply_link:
        for a in soup.find_all("a"):
            href = a.get("href", "")
            if href.startswith("http") and "sarkariresult" not in href:
                apply_link = href
                break

    # 🔁 Fallback
    if not apply_link:
        apply_link = fallback

    return apply_link


# ================= REGEX HELPERS =================

def extract(text, pattern):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "N/A"


def extract_number(text, pattern):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(2).strip()
    return "N/A"
