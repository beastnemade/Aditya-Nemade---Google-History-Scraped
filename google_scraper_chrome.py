from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv


class GoogleSearchScraper:
    """A class to handle Google search result extraction"""
    
    def __init__(self):
        self.browser = None
        self.wait_time = 10
        
    def initialize_browser(self):
        """Initialize Chrome browser with stealth configurations"""
        options = Options()
        # options.add_argument("--headless")  # Disabled for Windows compatibility
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            # Use system Chrome driver
            self.browser = webdriver.Chrome(options=options)
            print("Browser initialized successfully")
        except Exception as e:
            print(f"Error initializing browser: {e}")
            raise
        
    def perform_search(self, query_text):
        """Execute search query on Google"""
        try:
            print("Navigating to Google...")
            self.browser.get('https://www.google.com')
            time.sleep(3)
            
            print("Searching for query...")
            # Locate and interact with search input field
            input_field = WebDriverWait(self.browser, self.wait_time).until(
                EC.presence_of_element_located((By.NAME, 'q'))
            )
            input_field.clear()
            input_field.send_keys(query_text)
            input_field.submit()
            
            print("Waiting for results...")
            # Wait until results appear
            WebDriverWait(self.browser, self.wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.g'))
            )
            print("Results loaded successfully")
            
        except Exception as e:
            print(f"Error during search: {e}")
            raise
        
    def extract_result_data(self, result_element):
        """Extract information from a single search result"""
        data = {
            'title': '',
            'link': '',
            'snippet': ''
        }
        
        # Get title
        try:
            heading = result_element.find_element(By.CSS_SELECTOR, 'h3')
            data['title'] = heading.text
        except:
            data['title'] = 'N/A'
            
        # Get URL
        try:
            anchor = result_element.find_element(By.CSS_SELECTOR, 'a')
            data['link'] = anchor.get_attribute('href')
        except:
            data['link'] = 'N/A'
            
        # Get description
        description_selectors = ['div.VwiC3b', 'div.IsZvec', 'span.aCOpRe']
        for selector in description_selectors:
            try:
                desc_element = result_element.find_element(By.CSS_SELECTOR, selector)
                data['snippet'] = desc_element.text
                break
            except:
                continue
        
        if not data['snippet']:
            data['snippet'] = 'Description not available'
            
        return data
        
    def collect_results(self, max_results=10):
        """Gather all search results from the page"""
        collected_data = []
        
        try:
            result_containers = self.browser.find_elements(By.CSS_SELECTOR, 'div.g')
            
            for container in result_containers[:max_results]:
                try:
                    result_info = self.extract_result_data(container)
                    if result_info['title'] != 'N/A' and result_info['link'] != 'N/A':
                        collected_data.append(result_info)
                except Exception as error:
                    print(f"Error extracting result: {error}")
                    continue
                    
        except Exception as error:
            print(f"Error collecting results: {error}")
            
        return collected_data
        
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
            
    def cleanup(self):
        """Close browser and clean up resources"""
        if self.browser:
            self.browser.quit()
            
    def run(self, search_query, result_count=10):
        """Main execution method"""
        try:
            self.initialize_browser()
            self.perform_search(search_query)
            time.sleep(2)
            
            results = self.collect_results(result_count)
            self.display_results(results)
            self.save_to_file(results, 'scrapedgoogle.csv')
            
            return results
            
        except Exception as error:
            print(f"An error occurred: {error}")
            return []
            
        finally:
            self.cleanup()


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