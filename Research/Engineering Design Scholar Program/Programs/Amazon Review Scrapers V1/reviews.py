# Import packages
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

# Header to set the requests as a browser request
headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

# Function to get HTML from Amazon review page
def reviewsHtml(base_url):
    paginated_url = base_url
            #f"{base_url}&pageNumber={page_number}"
    print(f"Fetching URL: {paginated_url}")  # Debug print
    response = requests.get(paginated_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        return soup
    else:
        #print(f"Failed to fetch page {page_number}: Status code {response.status_code}")
        return None

# Function to extract reviews data from HTML
def getReviews(html_data):
    # Create Empty list to Hold all data
    data_dicts = []

    if html_data:
        # Select all Reviews BOX html using css selector
        boxes = html_data.select('div[data-hook="review"]')

        # Iterate all Reviews BOX
        for box in boxes:
            # Select Name using css selector and cleaning text using strip()
            # If Value is empty define value with 'N/A' for all.
            try:
                name = box.select_one('[class="a-profile-name"]').text.strip()
            except Exception:
                name = 'N/A'

            try:
                stars = box.select_one('[data-hook="review-star-rating"]').text.strip().split(' out')[0]
            except Exception:
                stars = 'N/A'

            try:
                title = box.select_one('[data-hook="review-title"]').text.strip()
            except Exception:
                title = 'N/A'

            try:
                # Convert date str to dd/mm/yyyy format
                datetime_str = box.select_one('[data-hook="review-date"]').text.strip().split(' on ')[-1]
                date = datetime.strptime(datetime_str, '%B %d, %Y').strftime("%d/%m/%Y")
            except Exception:
                date = 'N/A'

            try:
                description = box.select_one('[data-hook="review-body"]').text.strip()
            except Exception:
                description = 'N/A'

            # Create Dictionary with all review data
            data_dict = {
                'Name': name,
                'Stars': stars,
                'Title': title,
                'Date': date,
                'Description': description
            }

            # Add Dictionary in master empty List
            data_dicts.append(data_dict)

    return data_dicts

