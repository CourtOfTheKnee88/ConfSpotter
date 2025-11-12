import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urljoin
from datetime import datetime

# Small utilities for normalization
MONTHS = {m.lower(): i for i, m in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], start=1)}

# Helper functions for extraction and fetching
def extract_year(text):
    match = re.search(r'20\d{2}', text)
    return match.group(0) if match else ""

def parse_date_to_iso(month_name: str, day: int, year: int):
    try:
        # Normalize month name (accept full or abbreviated)
        month_num = datetime.strptime(month_name[:3], '%b').month
        return datetime(year, month_num, day).date().isoformat()
    except Exception:
        return ""


def parse_date_range(text: str):
    """Try several regex patterns to extract start and end dates and return ISO strings.

    Returns (start_iso, end_iso)
    """
    if not text:
        return "", ""

    # Patterns to match different common date ranges
    # Examples: "July 10-12, 2024" or "July 10, 2024 - July 12, 2024" or "10 July 2024"
    patterns = [
        # July 10-12, 2024
        r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2})-(\d{1,2}),?\s+(20\d{2})',
        # July 10, 2024 - July 12, 2024
        r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2}),?\s+(20\d{2})\s*[-–—]\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*(\d{1,2}),?\s*(20\d{2})',
        # 10 July 2024
        r'(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(20\d{2})',
        # July 10, 2024
        r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2}),?\s+(20\d{2})'
    ]

    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            try:
                if len(m.groups()) == 4:
                    # pattern 1: Mon Day-Day, Year
                    mon = m.group(1)
                    day1 = int(m.group(2))
                    day2 = int(m.group(3))
                    year = int(m.group(4))
                    start = parse_date_to_iso(mon, day1, year)
                    end = parse_date_to_iso(mon, day2, year)
                    return start, end
                elif len(m.groups()) == 6:
                    # pattern 2: Mon D, Y - Mon D, Y
                    mon1 = m.group(1); d1 = int(m.group(2)); y1 = int(m.group(3))
                    mon2 = m.group(4); d2 = int(m.group(5)); y2 = int(m.group(6))
                    start = parse_date_to_iso(mon1, d1, y1)
                    end = parse_date_to_iso(mon2, d2, y2)
                    return start, end
                elif len(m.groups()) == 3:
                    # pattern 3 or 4: Day Month Year  OR Month Day, Year
                    g1 = m.group(1); g2 = m.group(2); g3 = m.group(3)
                    # decide which is day vs month
                    if g1.isdigit():
                        day = int(g1); mon = g2; year = int(g3)
                    else:
                        mon = g1; day = int(g2); year = int(g3)
                    iso = parse_date_to_iso(mon, day, year)
                    return iso, ""
            except Exception:
                continue

    return "", ""


def normalize_location(raw: str):
    if not raw:
        return ""
    # remove labels and excessive whitespace, keep ',' separators
    raw = re.sub(r'(?i)^(Location|Place|Where|Venue)[:\s]*', '', raw).strip()
    raw = re.sub(r'\s*[-–—]\s*', ', ', raw)
    raw = re.sub(r'\s{2,}', ' ', raw)
    # remove trailing words like 'USA' leftover attached oddly
    return raw.strip(', ').strip()

def fetch_page_details(url):
    # Fetch the conference page and extract year, start_date, location
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return "", "", ""
        soup = BeautifulSoup(response.text, 'html.parser')
        year = extract_year(url) or extract_year(soup.title.string if soup.title else "")
        text = soup.get_text(separator=' ', strip=True)
        start_date, end_date = parse_date_range(text)
        # try common labeled location fields too
        loc_match = re.search(r'(?i)(Location|Place|Where|Venue)[:\s]+([^\n,\r]{3,200})', text)
        location = normalize_location(loc_match.group(2)) if loc_match else ""
        return year, start_date, end_date, location
    except Exception:
        return "", "", "", ""

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

        year, start_date, end_date, location = fetch_page_details(full_link)

        conferences.append({
            "source": "SIGCHI",
            "name": text,
            "link": full_link,
            "year": year,
            "start_date": start_date,
            "end_date": end_date,
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

        year, start_date, end_date, location = fetch_page_details(full_link)

        conferences.append({
            "source": "SIGPLAN",
            "name": text,
            "link": full_link,
            "year": year,
            "start_date": start_date,
            "end_date": end_date,
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
    # Basic cleaning/normalization pass
    def clean_name(n):
        if not n:
            return n
        # remove year-like suffixes in name (e.g., 'Conference 2024')
        n = re.sub(r'\(?20\d{2}\)?', '', n).strip()
        n = re.sub(r'\s{2,}', ' ', n)
        return n

    for c in all_confs:
        c['name'] = clean_name(c.get('name', ''))
        c['location'] = normalize_location(c.get('location', ''))
        # ensure year is four-digit or empty
        y = c.get('year', '') or ''
        c['year'] = y if re.match(r'^20\d{2}$', str(y)) else ''

    df = pd.DataFrame(all_confs)
    # drop exact duplicates by name+year+link
    df = df.drop_duplicates(subset=['name', 'year', 'link'])
    # Save both raw and normalized outputs
    df.to_csv("conferences.csv", index=False)
    df.to_csv("conferences_normalized.csv", index=False)
    print("\nSaved to conferences.csv and conferences_normalized.csv")

if __name__ == "__main__":
    main()
