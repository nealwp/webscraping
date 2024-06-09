import requests
from bs4 import BeautifulSoup
import csv

url = 'https://generations.global/speakers'

scraped_data = []

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    skibidiboop = soup.find_all('div', class_='HcOXKn')

    for fwip in skibidiboop:
        h5s = fwip.find_all('h5', class_='wixui-rich-text__text')
        for h5 in h5s:
            spans = h5.find_all('span', class_='wixui-rich-text__text')
            uniq_texts = sorted(list(set([s.get_text(strip=True) for s in spans])), key=len)

            if len(uniq_texts) == 4:
                uniq_texts.pop(0)
            data = {"name": uniq_texts[0], "title": uniq_texts[1]}
            scraped_data.append(data)
else:
    print("Failed to retrieve the webpage")

csv_file = 'genglobal.csv'

if scraped_data:
    with open(csv_file, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=['name', 'title'])
        dict_writer.writeheader()
        dict_writer.writerows(scraped_data)

    print(f"Data successfully written to {csv_file}")
else:
    print("No data to write to CSV.")
