import requests
import xml.etree.ElementTree as ET
import csv
from datetime import datetime
from dateutil import parser

# Fetch the RSS feed
url = 'https://news.google.com/rss/search?q=UChicago_Medicine'
response = requests.get(url)

# Parse the XML content
root = ET.fromstring(response.content)

# Define the cutoff date as a timezone-aware datetime
cutoff_date = datetime(2025, 1, 1).astimezone()  # Make it timezone-aware

# Open the CSV file for writing
with open('news_titles.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Link', 'Date'])  # Header row

    for item in root.findall('.//item'):
        title = item.find('title').text
        link = item.find('link').text
        pub_date = parser.parse(item.find('pubDate').text).astimezone()  # Convert to timezone-aware

        # Only include items from January 2025 onwards
        if pub_date >= cutoff_date:
            formatted_date = pub_date.strftime('%Y-%m-%d')
            writer.writerow([title, link, formatted_date])

print("News titles, links, and dates from January 2025 onwards have been saved to 'news_titles.csv'")
