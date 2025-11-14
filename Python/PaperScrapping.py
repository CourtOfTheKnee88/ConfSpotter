import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urljoin
from datetime import datetime
import mysql.connector

def fetch_conferences():
    # Fetch conferences from database
    connection = mysql.connector.connect(
        host='localhost', 
        user='ConfSpotter', 
        password='chickenlittle', 
        database='confspotter'
    )
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT CID, Title, link FROM Conferences WHERE link IS NOT NULL AND link != ''")
    conferences = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return conferences


def fetch_conference_papers(conference_link):
    # Try different common paths for call for papers
    potential_paths = [
        '/2026/calls',
        '/2026/call-for-papers',
        '/2026/cfp',
        '/2026/call',
        '/2026/participate',
        '/2026/papers',
        '/2026/participate/papers',
    ]
    
    papers = []
    
    valid_urls = []
    
    # First try the base URL and collect CFP links
    try:
        response = requests.get(conference_link, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Check if base URL has paper info
            papers.extend(extract_paper_deadlines(soup, conference_link))
            
            # Look for links that might lead to call for papers
            for link in soup.find_all('a', href=True):
                link_text = link.get_text().lower()
                href = link['href']
                
                if any(keyword in link_text for keyword in ['call for papers', 'cfp', 'calls', 'submissions', 'authors', 'submit', 'participate', 'papers']):
                    # Convert relative URLs to absolute
                    full_url = href if href.startswith('http') else urljoin(conference_link, href)
                    if full_url not in valid_urls:
                        valid_urls.append(full_url)
                        print(f"Found potential CFP link: {link.get_text()} -> {full_url}")
    except Exception as e:
        print(f"Error accessing base URL {conference_link}: {e}")
    
    # Try potential paths
    for path in potential_paths:
        try:
            if conference_link.endswith('/'):
                url = conference_link.rstrip('/') + path
            else:
                url = conference_link + path

            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                if url not in valid_urls:
                    valid_urls.append(url)
                    print(f"Success! Found call for papers at: {url}")
            else:
                print(f"  {url} - Status: {response.status_code}")
        except Exception as e:
            print(f"  {url} - Error: {e}")
    
    # Process all valid URLs found
    for url in valid_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                papers.extend(extract_paper_deadlines(soup, url))
        except Exception as e:
            print(f"Error processing {url}: {e}")

    return papers

def extract_paper_deadlines(soup, url):
    """Extract paper types and deadlines from CFP page"""
    found_papers = []
    
    # Enhanced date patterns to match the format in the example
    deadline_patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY or MM-DD-YYYY
        r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',    # YYYY/MM/DD or YYYY-MM-DD
        r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
        r'\b\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\b'     # DD Month YYYY
    ]
    
    # Look for "Important Dates" or similar sections
    page_text = soup.get_text()
    
    # Find sections that contain deadline information
    deadline_sections = []
    section_keywords = ['important dates', 'key dates', 'deadlines', 'timeline', 'schedule']
    
    for keyword in section_keywords:
        # Look for section headers
        section_pattern = rf'(?i){keyword}[^\n]*\n(.*?)(?=\n\n|\n[A-Z][^:\n]*:|$)'
        matches = re.finditer(section_pattern, page_text, re.DOTALL)
        for match in matches:
            deadline_sections.append(match.group(1))
            print(f"Found {keyword} section")
    
    # Process deadline sections
    for section in deadline_sections:
        lines = section.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for patterns like "Abstract: October 03, 2025" or "Full paper: October 10, 2025"
            deadline_line_patterns = [
                r'(abstract|full\s*paper|short\s*paper|poster|demo|workshop|tutorial|paper|submission|camera[-\s]*ready)[:\s]*(.*?)$',
                r'^(abstract|full\s*paper|short\s*paper|poster|demo|workshop|tutorial|paper|submission|camera[-\s]*ready)\s*[-:]?\s*(.*?)$'
            ]
            
            for pattern in deadline_line_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    paper_type = match.group(1).strip()
                    date_text = match.group(2).strip()
                    
                    # Look for dates in the date text
                    for date_pattern in deadline_patterns:
                        date_match = re.search(date_pattern, date_text, re.IGNORECASE)
                        if date_match:
                            found_papers.append({
                                'type': paper_type,
                                'deadline': date_match.group(0),
                                'source_url': url,
                                'context': line[:200]
                            })
                            print(f"Found in dates section: {paper_type} - Deadline: {date_match.group(0)}")
                            break
                    break
    
    # Look for tables that might contain deadline information
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                # Check if this row contains paper type and deadline info
                row_text = ' '.join([cell.get_text().strip() for cell in cells])
                
                # Look for paper types
                paper_types = ['abstract', 'full paper', 'short paper', 'poster', 'demo', 'workshop', 'tutorial', 'camera-ready', 'camera ready']
                
                for paper_type in paper_types:
                    if paper_type.lower() in row_text.lower():
                        # Found a paper type, now look for a date in this row
                        for pattern in deadline_patterns:
                            date_match = re.search(pattern, row_text, re.IGNORECASE)
                            if date_match:
                                found_papers.append({
                                    'type': paper_type,
                                    'deadline': date_match.group(0),
                                    'source_url': url,
                                    'context': row_text[:200]
                                })
                                print(f"Found in table: {paper_type} - Deadline: {date_match.group(0)}")
                                break
    
    # Also look for deadline information in regular text (general patterns)
    deadline_phrases = [
        r'(abstract|full\s*paper|short\s*paper|poster|demo|workshop|tutorial|camera[-\s]*ready)\s+(deadline|due|submission)[:\s]*([^.\n]{10,50})',
        r'(deadline|due\s*date)[:\s]*(abstract|full\s*paper|short\s*paper|poster|demo|workshop|tutorial|camera[-\s]*ready)[:\s]*([^.\n]{10,50})',
        r'(submit|submission)\s+(abstract|full\s*paper|short\s*paper|poster|demo|workshop|tutorial|camera[-\s]*ready)[:\s]*([^.\n]{10,50})'
    ]
    
    for phrase_pattern in deadline_phrases:
        matches = re.finditer(phrase_pattern, page_text, re.IGNORECASE)
        for match in matches:
            # Determine paper type and deadline text based on match groups
            groups = match.groups()
            if len(groups) >= 3:
                if 'abstract' in groups[0].lower() or 'paper' in groups[0].lower() or 'poster' in groups[0].lower():
                    paper_type = groups[0]
                    deadline_text = groups[2]
                else:
                    paper_type = groups[1]
                    deadline_text = groups[2]
            else:
                paper_type = groups[0] if groups else 'unknown'
                deadline_text = match.group(0)
            
            # Look for dates in the deadline text
            for pattern in deadline_patterns:
                date_match = re.search(pattern, deadline_text, re.IGNORECASE)
                if date_match:
                    found_papers.append({
                        'type': paper_type,
                        'deadline': date_match.group(0),
                        'source_url': url,
                        'context': match.group(0)[:200]
                    })
                    print(f"Found in general text: {paper_type} - Deadline: {date_match.group(0)}")
                    break
    
    return found_papers

def main():
    conferences = fetch_conferences()
    all_papers = []
    
    for conference in conferences:
        conference_link = conference['link']
        print(f"\nFetching papers for conference: {conference['Title']} ({conference_link})")
        papers = fetch_conference_papers(conference_link)
        
        # Add conference info to each paper
        for paper in papers:
            paper['conference_title'] = conference['Title']
            paper['conference_id'] = conference['CID']
        
        all_papers.extend(papers)
    
    # Print summary of all found papers
    print(f"\n{'='*60}")
    print(f"SUMMARY: Found {len(all_papers)} papers across {len(conferences)} conferences")
    print(f"{'='*60}")
    
    for paper in all_papers:
        print(f"\nConference: {paper['conference_title']}")
        print(f"Paper Type: {paper['type']}")
        print(f"Deadline: {paper['deadline']}")
        print(f"Source URL: {paper['source_url']}")
        print(f"Context: {paper['context'][:100]}...")
        print("-" * 40)
    
    # Save papers to CSV
    if all_papers:
        df = pd.DataFrame(all_papers)
        df.to_csv("papers.csv", index=False)
        print(f"\nSaved {len(all_papers)} papers to papers.csv")
    else:
        print("\nNo papers found to save to CSV")

if __name__ == "__main__":
    main()