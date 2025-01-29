import requests
import xml.etree.ElementTree as ET
import csv
from datetime import datetime
from dateutil import parser

# Input and output file paths
input_csv = 'keywords.csv'
output_csv = 'news_results.csv'

# Define cutoff date
cutoff_date = datetime(2025, 1, 1).astimezone()  # Ensure timezone-aware

# Open the output CSV for writing
with open(output_csv, 'w', newline='', encoding='utf-8') as out_file:
    writer = csv.writer(out_file)
    writer.writerow(['Keyword', 'Title', 'Link', 'Date'])  # Header row

    # Read keywords from the input CSV
    with open(input_csv, 'r', newline='', encoding='utf-8-sig') as in_file:  # Handle BOM
        reader = csv.DictReader(in_file)
        print(f"CSV Headers: {reader.fieldnames}")  # Debug: Check headers

        for row in reader:
            try:
                keyword = row['Keyword']  # Update this if column name differs
            except KeyError:
                print("Error: 'Keyword' column not found. Check the input CSV.")
                break

            print(f"Searching for keyword: {keyword}")

            # Fetch the RSS feed for the keyword
            url = f'https://news.google.com/rss/search?q={keyword}'
            response = requests.get(url)

            # Parse the XML content
            root = ET.fromstring(response.content)

            # Process each news item in the feed
            for item in root.findall('.//item'):
                title = item.find('title').text
                link = item.find('link').text
                pub_date = parser.parse(item.find('pubDate').text).astimezone()  # Ensure timezone-aware

                # Filter articles by cutoff date
                if pub_date >= cutoff_date:
                    formatted_date = pub_date.strftime('%Y-%m-%d')
                    writer.writerow([keyword, title, link, formatted_date])

print(f"Results have been saved to '{output_csv}'")
