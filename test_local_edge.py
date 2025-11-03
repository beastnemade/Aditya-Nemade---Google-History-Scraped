from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time

def test_local_edge():
    """Test using system Edge driver"""
    try:
        print("Setting up Edge options...")
        options = Options()
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        print("Starting Edge browser with system driver...")
        # Try using system Edge driver without webdriver-manager
        browser = webdriver.Edge(options=options)
        
        print("Navigating to Google...")
        browser.get('https://www.google.com')
        time.sleep(3)
        
        print(f"Page title: {browser.title}")
        print("Test successful!")
        
        browser.quit()
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    test_local_edge()