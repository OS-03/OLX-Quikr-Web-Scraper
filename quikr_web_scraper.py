import scrapy
from scrapy.crawler import CrawlerProcess
import json

class Quikr(scrapy.Spider):
    name = 'quikr'

    url = 'https://www.quikr.com/cars/used+Maruti-Suzuki+Swift+cars+all-india+z1399vbd?page=21&aj=1&assuredfrom=0&premiumfrom=0&goldfrom=0&basicfrom=43&assuredcount=0&premiumcount=0&goldcount=0&basiccount=24'

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    def __init__(self):
        with open('results.json', 'w') as json_file:
            json.dump([], json_file)

    def start_requests(self):
            yield scrapy.Request(url=self.url + '&page=' + str(page), headers=self.headers, callback=self.parse)

    def parse(self, res):
        data = json.loads(res.text)
        # Print the keys to inspect structure
        print("Top-level keys:", data.keys())
        if 'data' in data and 'records' in data['data']:
            offers = data['data']['records']
        else:
            print("No records found in response.")
            return

        items_list = []
        for offer in offers:
            if not isinstance(offer, dict):
                print(f"Skipping non-dict offer: {offer}")
                continue
            items = {
                'title': offer.get('title', ''),
                'description': offer.get('description', '').replace('\n', ' '),
                'price': (
                    offer.get('price', '')
                    if isinstance(offer.get('price', ''), str)
                    else offer.get('price', {}).get('value', {}).get('display', '')
                )
            }
            print(json.dumps(items, indent=2))
            items_list.append(items)
        # Append to JSON file
        if items_list:
            with open('results.json', 'w+') as json_file:
                try:
                    existing = json.load(json_file)
                except json.JSONDecodeError:
                    existing = []
                existing.extend(items_list)
                json_file.seek(0)
                json.dump(existing, json_file, indent=2)
                json_file.truncate()

# run scraper
process = CrawlerProcess()
process.crawl(Quikr)
process.start()
