import time
import feedparser
import pandas as pd
import csv
import os
from newsplease import NewsPlease

# Example RSS feeds for financial news
rss_feeds = [
    'https://www.cnbc.com/id/100003114/device/rss/rss.html',  # CNBC
    'https://feeds.reuters.com/reuters/businessNews',         # Reuters
    'https://www.bloomberg.com/feed/podcast/decrypted.xml',   # Bloomberg
    'https://feeds.marketwatch.com/marketwatch/topstories',   # MarketWatch
    'https://www.ft.com/rss/homepage',                        # Financial Times
    'https://www.investing.com/rss/news.rss',                 # Investing.com
    'https://www.forbes.com/most-popular/feed/',              # Forbes
    'https://www.theguardian.com/uk/business/rss',            # The Guardian
    'https://www.wsj.com/xml/rss/3_7014.xml',                 # Wall Street Journal
    'https://www.economist.com/business/rss.xml',             # The Economist
    'https://seekingalpha.com/feed.xml',                      # Seeking Alpha
    'https://www.businessinsider.com/sai/rss',                # Business Insider
    'https://www.moneycontrol.com/rss/latestnews.xml',        # Moneycontrol
    'https://www.zacks.com/rss/zacks_investment_research.xml' # Zacks
]

# CSV file to store scraped data
csv_file = "financial_news_articles.csv"
visited_urls_file = "visited_urls.txt"

# Initialize a DataFrame to store articles
columns = ["title", "text", "publish_date", "url", "source_brand"]
data = pd.DataFrame(columns=columns)

# Function to save data to CSV
def save_to_csv(df, file):
    try:
        df.to_csv(file, index=False, mode='a', header=not os.path.exists(file), quoting=csv.QUOTE_ALL)
    except Exception as e:
        print(f"Error saving to CSV: {e}")

# Function to load visited URLs from a file
def load_visited_urls(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return set(line.strip() for line in f)
    return set()

# Function to save visited URLs to a file
def save_visited_urls(urls, file):
    with open(file, "w") as f:
        f.writelines(f"{url}\n" for url in urls)

# Function to fetch RSS articles
def fetch_rss_articles(rss_urls):
    articles = []
    for url in rss_urls:
        print(f"Fetching RSS feed from {url}")
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                if 'published' in entry:  # Filter recent articles
                    articles.append({
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.published
                    })
        except Exception as e:
            print(f"Error fetching RSS feed from {url}: {e}")
    return articles

# Function to fetch and process articles from RSS feeds
def process_articles(rss_urls, visited_urls):
    articles = fetch_rss_articles(rss_urls)
    new_visited_urls = set()
    for article in articles:
        if article['link'] not in visited_urls:
            try:
                # Extract article using NewsPlease
                extracted_article = NewsPlease.from_url(article['link'])

                if extracted_article and extracted_article.title and extracted_article.maintext:
                    # Append article data
                    article_data = {
                        "title": extracted_article.title,
                        "text": extracted_article.maintext,
                        "publish_date": extracted_article.date_publish,
                        "url": article['link'],
                        "source_brand": extracted_article.source_domain
                    }
                    print(article_data)

                    # Add to DataFrame
                    df = pd.DataFrame([article_data])

                    # Save to CSV
                    save_to_csv(df, csv_file)

                    print(f"Saved article: {extracted_article.title}")

                    # Add URL to visited set
                    new_visited_urls.add(article['link'])

            except Exception as e:
                print(f"Error processing article {article['link']}: {e}")
    return new_visited_urls

# Infinite scraping loop
try:
    visited_urls = load_visited_urls(visited_urls_file)

    while True:
        new_visited_urls = process_articles(rss_feeds, visited_urls)
        visited_urls.update(new_visited_urls)
        save_visited_urls(visited_urls, visited_urls_file)

        # Wait before next iteration to avoid overwhelming servers
        time.sleep(300)  # 5-minute interval

except KeyboardInterrupt:
    print("Scraping stopped by user.")
    save_visited_urls(visited_urls, visited_urls_file)
