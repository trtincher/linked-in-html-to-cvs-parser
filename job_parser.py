import csv
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import re

class LinkedInJobParser:
    def __init__(self, html_file: str):
        self.html_file = html_file
        self.debug = True
        
    def extract_jobs_from_html(self) -> List[Dict[str, Any]]:
        """Extract job listings from LinkedIn HTML file."""
        with open(self.html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        job_listings = []
        
        # Find the job list container
        job_list = soup.find('ul', class_='eUqfEYGWzKYSSZZiKvAmRbkGoCLfJrzzPwBhk')
        if not job_list:
            print("Could not find job list container")
            return job_listings
            
        # Find all job items
        job_items = job_list.find_all('li', class_='ember-view')
        print(f"Found {len(job_items)} potential job items")
        
        for idx, item in enumerate(job_items, 1):
            if self.debug:
                print(f"\nProcessing job {idx}/{len(job_items)}")
            job = self._parse_job_card(item)
            if job:
                job_listings.append(job)
            elif self.debug:
                print(f"Job {idx} was skipped")
                
        return job_listings
    
    def _parse_job_card(self, item) -> Dict[str, Any]:
        """Parse individual job card HTML."""
        try:
            # Get job ID
            job_id = item.get('data-occludable-job-id', '')
            if self.debug:
                print(f"Processing job ID: {job_id}")
            
            # Find the job card container div by looking for data-job-id
            card = None
            for div in item.find_all('div', recursive=True):
                if div.get('data-job-id') == job_id and 'job-card-container' in div.get('class', []):
                    card = div
                    break
            
            if not card:
                if self.debug:
                    print("Could not find job-card-container div")
                return None
            
            # Get job title
            title = ''
            title_elem = card.find('a', class_=lambda x: x and 'job-card-container__link' in x)
            if title_elem:
                # Try to find the text within a strong tag first
                strong = title_elem.find('strong')
                if strong:
                    # Get text content excluding any verification badges
                    title = ''.join(t for t in strong.contents if isinstance(t, str)).strip()
            
            if not title and self.debug:
                print("Could not find job title")
            
            # Get company name
            company = ''
            subtitle_div = card.find('div', class_='artdeco-entity-lockup__subtitle')
            if subtitle_div:
                company_span = subtitle_div.find('span', class_='lhTobqFRnhXjIxsPALxnKZTvtIokoQuCLO')
                if company_span:
                    company = company_span.get_text(strip=True)
            
            if not company and self.debug:
                print("Could not find company name")
            
            # Get location
            location = ''
            metadata_wrapper = card.find('ul', class_='job-card-container__metadata-wrapper')
            if metadata_wrapper:
                location_li = metadata_wrapper.find('li', class_='nnOoYztMdggrEcztrGDGSlUMxBgYhtrXQEvk')
                if location_li:
                    location = location_li.get_text(strip=True)
            
            if not location and self.debug:
                print("Could not find location")
            
            # Get workplace type
            workplace_type = "Remote" if location and "Remote" in location else "On-site"
            
            # Get salary information
            salary = ''
            metadata_div = card.find('div', class_='artdeco-entity-lockup__metadata')
            if metadata_div:
                metadata_list = metadata_div.find('ul', class_='job-card-container__metadata-wrapper')
                if metadata_list:
                    salary_li = metadata_list.find('li', class_='nnOoYztMdggrEcztrGDGSlUMxBgYhtrXQEvk')
                    if salary_li:
                        salary = salary_li.get_text(strip=True)
            
            # Get application link
            apply_url = title_elem.get('href', '') if title_elem else ''
            
            # Get posting metadata
            metadata = {}
            
            # Find footer
            footer = card.find('ul', class_=lambda x: x and 'job-card-list__footer-wrapper' in x)
            if footer:
                # Get posting time
                time_elem = footer.find('time')
                if time_elem:
                    metadata['posted'] = time_elem.get_text(strip=True)
                
                # Check for Easy Apply
                easy_apply = footer.find(string=re.compile('Easy Apply'))
                metadata['easy_apply'] = bool(easy_apply)
                
                # Check for Promoted tag
                promoted = footer.find(string=re.compile('Promoted'))
                metadata['promoted'] = bool(promoted)
            
            # Get additional insights
            insights = ''
            insights_div = card.find('div', class_='job-card-list__insight')
            if insights_div:
                insights_text = insights_div.find('div', class_='job-card-container__job-insight-text')
                if insights_text:
                    insights = insights_text.get_text(strip=True)
            
            if not title or not company:
                if self.debug:
                    print(f"Missing required fields - Title: {bool(title)}, Company: {bool(company)}")
                return None
                
            job_data = {
                'job_id': job_id,
                'title': title,
                'company': company,
                'location': location,
                'workplace_type': workplace_type,
                'salary': salary,
                'apply_url': apply_url,
                'posted': metadata.get('posted', ''),
                'easy_apply': metadata.get('easy_apply', False),
                'promoted': metadata.get('promoted', False),
                'insights': insights
            }
            
            if self.debug:
                print(f"Successfully parsed job: {title} at {company}")
            
            return job_data
            
        except Exception as e:
            if self.debug:
                print(f"Error parsing job card: {str(e)}")
            return None
    
    def save_to_csv(self, jobs: List[Dict[str, Any]], output_file: str):
        """Save job listings to CSV file."""
        if not jobs:
            print("No jobs to save")
            return
            
        fieldnames = ['job_id', 'title', 'company', 'location', 'workplace_type',
                     'salary', 'apply_url', 'posted', 'easy_apply', 'promoted', 'insights']
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for job in jobs:
                if job:  # Only write valid job entries
                    writer.writerow(job)
        
        print(f"Successfully saved {len(jobs)} jobs to {output_file}")

def main():
    parser = LinkedInJobParser('job-search.html')
    jobs = parser.extract_jobs_from_html()
    parser.save_to_csv(jobs, 'linkedin_jobs.csv')
    print(f"Found {len(jobs)} job listings")

if __name__ == "__main__":
    main() 