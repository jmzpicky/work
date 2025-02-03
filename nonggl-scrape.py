import requests
import csv
from datetime import datetime

# Your NewsAPI key (replace with your own key)
API_KEY = '8e97df55da4a4f308ef2e210eab071e7'

# Function to fetch articles using NewsAPI
def get_news_articles(query):
    # Construct the NewsAPI URL (removing date filter for now)
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}"
    print(f"API URL: {url}")  # Debug: Print the API request URL

    # Send the GET request
    response = requests.get(url)

    # Debugging the response status and content
    print(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response Data: {data}")  # Debug: Print the response data to check structure

        results = []

        # Iterate through articles if available
        for article in data.get('articles', []):
            title = article.get('title')
            link = article.get('url')
            pub_date = article.get('publishedAt')

            # Debug: Print each article data
            print(f"Found article: {title} ({pub_date}) - {link}")

            # Add the article to the results
            results.append([query, title, link, pub_date])

        return results
    else:
        print(f"Failed to fetch data from API. Status Code: {response.status_code}, Response: {response.text}")
        return []  # Return an empty list if API call failed

# Output file path
output_csv = 'new_results.csv'

# Open the output CSV for writing
with open(output_csv, 'w', newline='', encoding='utf-8') as out_file:
    writer = csv.writer(out_file)
    writer.writerow(['Keyword', 'Title', 'Source Link', 'Date'])  # Header row

    total_links = 0  # Initialize the total link counter

    # Open the input CSV containing keywords
    with open('keywords.csv', 'r', newline='', encoding='utf-8-sig') as in_file:
        reader = csv.DictReader(in_file)
        print(f"CSV Headers: {reader.fieldnames}")  # Debug: Check headers

        # For each row (keyword) in the input CSV
        for row in reader:
            keyword = row['Keyword']  # Ensure this matches the column name in your 'keywords.csv'
            print(f"Searching for keyword: {keyword}")

            # Fetch articles using NewsAPI
            results = get_news_articles(keyword)

            # If results are found, write them to the CSV and count them
            if results:
                for result in results:
                    writer.writerow(result)

                num_links = len(results)
                total_links += num_links
                print(f"Extracted {num_links} links for keyword: {keyword}")
            else:
                print(f"No articles found for keyword: {keyword}")

    print(f"Total links extracted: {total_links}")
    
print(f"Results have been saved to '{output_csv}'")
