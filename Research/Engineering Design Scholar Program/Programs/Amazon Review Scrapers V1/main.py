# main_script.py

import pandas as pd
from reviews import reviewsHtml, getReviews

"""
# Parameters
input_file = 'original_urls.txt'
output_file = 'review_urls.txt'
extractingPages = 5

def generate_paged_links(input_file, output_file, extractingPages):
    with open(input_file, 'r') as infile:
        original_urls = infile.readlines()

    with open(output_file, 'w') as outfile:
        for url in original_urls:
            url = url.strip()
            for page in range(1, extractingPages + 1):
                paged_url = f"{url}&pageNumber={page}"
                outfile.write(paged_url + '\n')

# Generate links
generate_paged_links(input_file, output_file, extractingPages)
"""

# Main script to read URLs from file and process each
with open('review_urls.txt', 'r') as file:
    urls = file.readlines()


for idx, url in enumerate(urls):
    url = url.strip()  # Remove any leading/trailing whitespace
    all_reviews = []
    html_data = reviewsHtml(url)
    if html_data:
        reviews = getReviews(html_data)
        all_reviews.extend(reviews)
    if all_reviews:
        df_reviews = pd.DataFrame(all_reviews)
        output_filename = f'reviews_{idx + 1}.csv'
        df_reviews.to_csv(output_filename, index=False)
        print(f"Scraped reviews for URL {url} and saved to {output_filename}")
    else:
        print(f"No reviews found for URL {url}")
