import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Initialize an empty list to collect all headings
all_headings = []

page = 1
while True:
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Will raise HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        break

    soup = BeautifulSoup(response.text, "lxml")

    # Check if this is the last page
    if not soup.find('li', class_='next'):
        break

    # Extract and process data within the loop
    headings = soup.find_all('h3')
    for heading in headings:
        all_headings.append(heading.text.strip())

    page += 1
    time.sleep(2)  # Sleep for 2 seconds to avoid overwhelming the website

# After the loop, save all collected headings to a CSV file
data = {"Headings": all_headings}
df = pd.DataFrame(data)
df.to_csv("headings.csv", index=False)