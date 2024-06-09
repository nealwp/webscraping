import requests
from bs4 import BeautifulSoup
import csv

url = 'https://gn-midsouth.com/gnmidsouth-directory'

scraped_data = []
for page in range(12):
    response = requests.get(url + f'/page/{page+1}')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        listings = soup.find_all('div', class_='listing-details')

        for listing in listings:
            listing_data = {}
            labels = listing.find_all('span', class_='field-label')
            values = listing.find_all('div', class_='value')

            for label, value in zip(labels, values):
                key = label.get_text(strip=True)
                value_text = value.get_text(strip=True)
                listing_data[key] = value_text

            scraped_data.append(listing_data)

    else:
        print("Failed to retrieve the webpage")

all_keys = set()
for data in scraped_data:
    all_keys.update(data.keys())

csv_file = 'gn-midsouth-directory.csv'

if scraped_data:
    with open(csv_file, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=all_keys)
        dict_writer.writeheader()
        dict_writer.writerows(scraped_data)

    print(f"Data successfully written to {csv_file}")
else:
    print("No data to write to CSV.")
