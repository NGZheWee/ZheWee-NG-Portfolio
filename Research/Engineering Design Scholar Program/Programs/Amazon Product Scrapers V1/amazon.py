"""
from selectorlib import Extractor
import requests
import csv
import json
from time import sleep


# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('selectors.yml')

def scrape(url):

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create
    return e.extract(r.text)

# Read URLs from file and scrape data
with open("urls.txt", 'r') as urllist, open('output.csv', 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    header_written = False
    for url in urllist.read().splitlines():
        data = scrape(url)
        if data:
            if not header_written:
                writer.writerow(data.keys())
                header_written = True
            writer.writerow(data.values())
            # sleep(5)
"""
from selectorlib import Extractor
import requests
import csv
import json
from time import sleep

# Create an Extractor by reading from the updated YAML file
e = Extractor.from_yaml_file('selectors.yml')

def scrape(url):
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s" % url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d" % (url, r.status_code))
        return None
    # Pass the HTML of the page and create
    extracted_data = e.extract(r.text)
    if extracted_data:
        extracted_data['product_page_url'] = url
    return extracted_data

# Read URLs from file and scrape data
with open("urls.txt", 'r') as urllist, open('output.csv', 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    header_written = False
    for url in urllist.read().splitlines():
        data = scrape(url)
        if data:
            # Remove unwanted fields
            data.pop('sales_rank', None)
            data.pop('product_description', None)
            data.pop('variants', None)

            # Clean number of reviews text
            if 'number_of_reviews' in data and data['number_of_reviews']:
                data['number_of_reviews'] = data['number_of_reviews'].replace('ratings', '').replace(',', '').strip()

            # Rename short_description to description
            if 'short_description' in data:
                data['description'] = data.pop('short_description')

            # Handle missing price data
            if 'price' not in data or not data['price']:
                data['price'] = 'N/A'

            # Rearrange the columns in the desired order
            ordered_data = {
                'name': data.get('name'),
                'images': data.get('images'),
                'price': data.get('price'),
                'product_dimensions': data.get('product_dimensions'),
                'description': data.get('description'),
                'sustainability_features': data.get('sustainability_features'),
                'rating': data.get('rating'),
                'number_of_reviews': data.get('number_of_reviews'),
                'product_page_url': data.get('product_page_url')
            }

            if not header_written:
                writer.writerow(ordered_data.keys())
                header_written = True
            writer.writerow(ordered_data.values())
            # sleep(5)






# product_data = []
#with open("urls.txt",'r') as urllist, open('output.jsonl','w') as outfile:
    #for url in urllist.read().splitlines():
        #data = scrape(url)
        #if data:
            #json.dump(data,outfile)
            #outfile.write("\n")
            # sleep(5)





    