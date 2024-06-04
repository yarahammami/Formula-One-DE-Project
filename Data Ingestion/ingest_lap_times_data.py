from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run in headless mode (no browser UI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL of the webpage to scrape
url = 'https://f1-dash.com/dashboard'

# Fetch the webpage content
driver.get(url)

# Wait for the content to load (adjust time as needed)
time.sleep(5)  # Adjust this depending on the website's loading time

# Find all <p> tags with the specific class
lap_times_elements = driver.find_elements(By.CLASS_NAME, 'text-lg.font-semibold.leading-none')

# Extract and print the text from each <p> tag
for lap_time_element in lap_times_elements:
    print(lap_time_element.text)

# Quit the driver
driver.quit()
