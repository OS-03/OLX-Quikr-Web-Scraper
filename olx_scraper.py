from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import csv
import time

url = 'https://www.olx.in/api/relevance/search?category=1725&facet_limit=100&location=1000001&location_facet_limit=20&user=1708c08dd02x5e692f19'

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

# Setup Selenium with headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(f"user-agent={headers['user-agent']}")
driver = webdriver.Chrome(options=chrome_options)

# Create CSV with header
with open('results.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['title', 'description', 'location', 'features', 'date', 'price'])

for page in range(0, 5):
    api_url = url + '&page=' + str(page)
    driver.get(api_url)
    time.sleep(2)  # Wait for the page to load

    # Get the raw JSON response from the page
    pre = driver.find_element("tag name", "pre")
    data = json.loads(pre.text)

    for offer in data.get('data', []):
        items = {
            'title': offer.get('title', ''),
            'description': offer.get('description', '').replace('\n', ' '),
            'location': ', '.join([
                offer.get('locations_resolved', {}).get('COUNTRY_name', ''),
                offer.get('locations_resolved', {}).get('ADMIN_LEVEL_1_name', ''),
                offer.get('locations_resolved', {}).get('ADMIN_LEVEL_3_name', ''),
                offer.get('locations_resolved', {}).get('SUBLOCALITY_LEVEL_1_name', '')
            ]),
            'features': offer.get('main_info', ''),
            'date': offer.get('display_date', ''),
            'price': offer.get('price', {}).get('value', {}).get('display', '')
        }
        print(json.dumps(items, indent=2, ensure_ascii=False))
        with open('results.csv', 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=items.keys())
            writer.writerow(items)

driver.quit()
