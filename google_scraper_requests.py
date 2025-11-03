import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from urllib.parse import urlencode


class GoogleSearchScraper:
    """A class to handle Google search result extraction using requests"""
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers.update(self.headers)
        
    def perform_search(self, query_text, num_results=10):
        """Execute search query on Google"""
        try:
            print(f"Searching for: {query_text}")
            
            # Build Google search URL
            params = {
                'q': query_text,
                'num': num_results,
                'hl': 'en'
            }
            url = f"https://www.google.com/search?{urlencode(params)}"
            
            # Add random delay to avoid being blocked
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(url)
            response.raise_for_status()
            
            print("Search completed successfully")
            return response.text
            
        except Exception as e:
            print(f"Error during search: {e}")
            raise
        
    def extract_results(self, html_content):
        """Extract search results from HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        
        # Find search result containers
        search_results = soup.find_all('div', class_='g')
        
        for result in search_results:
            try:
                # Extract title
                title_elem = result.find('h3')
                title = title_elem.get_text() if title_elem else 'N/A'
                
                # Extract link
                link_elem = result.find('a')
                link = link_elem.get('href') if link_elem else 'N/A'
                
                # Extract snippet
                snippet_elem = result.find('span', class_='aCOpRe') or result.find('div', class_='VwiC3b')
                snippet = snippet_elem.get_text() if snippet_elem else 'Description not available'
                
                if title != 'N/A' and link != 'N/A':
                    results.append({
                        'title': title,
                        'link': link,
                        'snippet': snippet
                    })
                    
            except Exception as e:
                print(f"Error extracting result: {e}")
                continue
                
        return results
        
    def save_to_file(self, data, filename='search_results.csv'):
        """Export collected data to CSV file"""
        if not data:
            print("No data to save")
            return
            
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            column_names = ['title', 'link', 'snippet']
            csv_writer = csv.DictWriter(csvfile, fieldnames=column_names)
            csv_writer.writeheader()
            csv_writer.writerows(data)
            
        print(f"Successfully saved {len(data)} entries to {filename}")
        
    def display_results(self, data):
        """Print results to console"""
        if not data:
            print("No results to display")
            return
            
        print("\n" + "="*80)
        print("SEARCH RESULTS")
        print("="*80 + "\n")
        
        for idx, item in enumerate(data, 1):
            print(f"Result #{idx}")
            print(f"Title: {item['title']}")
            print(f"URL: {item['link']}")
            print(f"Description: {item['snippet']}")
            print("-" * 80 + "\n")
            
    def run(self, search_query, result_count=10):
        """Main execution method"""
        try:
            html_content = self.perform_search(search_query, result_count)
            results = self.extract_results(html_content)
            
            self.display_results(results)
            self.save_to_file(results, 'scrapedgoogle.csv')
            
            return results
            
        except Exception as error:
            print(f"An error occurred: {error}")
            return []


def execute_scraper():
    """Entry point for the application"""
    user_query = input("Please enter your search query: ")
    
    if not user_query.strip():
        print("Search query cannot be empty!")
        return
        
    scraper = GoogleSearchScraper()
    scraper.run(user_query)


if __name__ == "__main__":
    execute_scraper()