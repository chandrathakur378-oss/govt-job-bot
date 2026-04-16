import requests
from bs4 import BeautifulSoup

URL = "https://www.sarkariresult.com/"

def fetch_jobs():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")

    jobs = []
    jobs += extract_section(soup, "Latest Jobs", "latest_job")
    jobs += extract_section(soup, "Admit Card", "admit_card")
    jobs += extract_section(soup, "Result", "result")

    return jobs


def extract_section(soup, name, category):
    jobs = []

    for h in soup.find_all("div"):
        if name.lower() in h.text.lower():
            ul = h.find_next("ul")

            if not ul:
                continue

            for li in ul.find_all("li"):
                a = li.find("a")
                if not a:
                    continue

                jobs.append({
                    "title": a.text.strip(),
                    "url": a.get("href"),
                    "category": category
                })

    return jobs