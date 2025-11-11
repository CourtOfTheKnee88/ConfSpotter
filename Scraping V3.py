import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urljoin

# Helper functions for extraction and fetching
def extract_year(text):
    match = re.search(r'20\d{2}', text)
    return match.group(0) if match else ""

def extract_dates_location(soup):
    # Try to find conference dates and location from the page text
    text = soup.get_text(separator=' ', strip=True)
    
    # Attempt to find start date
    date_match = re.search(r'(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2}(?:-\d{1,2})?,?\s+20\d{2})', text)
    start_date = date_match.group(1) if date_match else ""
    
    # Attempt to find location
    loc_match = re.search(r'(Location|Place|Where)[:\s]+([A-Za-z ,]+)', text)
    location = loc_match.group(2).strip() if loc_match else ""

    return start_date, location

def fetch_page_details(url):
    # Fetch the conference page and extract year, start_date, location
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        year = extract_year(url) or extract_year(soup.title.string if soup.title else "")
        start_date, location = extract_dates_location(soup)
        return year, start_date, location
    except Exception:
        return "", "", ""

# SIGCHI
def fetch_sigchi_conferences():
    url = "https://sigchi.org/conferences/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    conferences = []
    seen_links = set()

    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        href = a["href"]

        # Skip empty or too short links
        if not text or len(text) < 3 or href in seen_links:
            continue

        # for use in eliminating links deemed as "non-conference links"
        exclude_keywords = [
            "what is sigchi", "upcoming conference", "conference history", "publications", "ethics and conduct", "policies", "policy",
            "cares", "voting history", "contact us", "membership", "executive committee", "all committees", "chapters", "awards", "guides",
            "blog", "meetings", "announcements", "volunteer history", "open calls", "development fund", "digital library", "join us",
            "calendar", "updates", "application forms", "programs app", "youtube", "home", "about", "news", "events"
        ]
        if any(kw in text.lower() for kw in exclude_keywords):
            continue

        seen_links.add(href)
        full_link = href if href.startswith("http") else urljoin("https://sigchi.org", href)

        year, start_date, location = fetch_page_details(full_link)

        conferences.append({
            "source": "SIGCHI",
            "name": text,
            "link": full_link,
            "year": year,
            "start_date": start_date,
            "end_date": "",
            "location": location
        })

    return conferences

# SIGPLAN
def fetch_sigplan_conferences():
    url = "https://sigplan.org/Conferences"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    conferences = []
    seen_links = set()

    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        href = a["href"]

        # Skip empty or very short links
        if not text or len(text) < 3 or href in seen_links:
            continue

        # for use in eliminating links deemed as "non-conference links"
        exclude_keywords = [
            "home", "about", "contact", "news", "conferences", "jobs", "awards", "opentoc", "sigplan", "research highlights",
            "membership", "calendar", "organizers"
        ]
        if any(kw in text.lower() for kw in exclude_keywords):
            continue

        seen_links.add(href)
        full_link = href if href.startswith("http") else urljoin("https://sigplan.org", href)

        year, start_date, location = fetch_page_details(full_link)

        conferences.append({
            "source": "SIGPLAN",
            "name": text,
            "link": full_link,
            "year": year,
            "start_date": start_date,
            "end_date": "",
            "location": location
        })

    return conferences

def main():
    print("Fetching SIGCHI conferences...")
    sigchi_confs = fetch_sigchi_conferences()
    print(f"Found {len(sigchi_confs)} SIGCHI conferences.")

    print("Fetching SIGPLAN conferences...")
    sigplan_confs = fetch_sigplan_conferences()
    print(f"Found {len(sigplan_confs)} SIGPLAN conferences.")

    all_confs = sigchi_confs + sigplan_confs
    df = pd.DataFrame(all_confs)

    df.to_csv("conferences.csv", index=False)
    print("\nSaved to conferences.csv")

if __name__ == "__main__":
    main()
