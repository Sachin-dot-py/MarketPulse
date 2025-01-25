import newspaper
import os
import json

# Persistent storage file for visited links
VISITED_LINKS_FILE = "visited_links.json"

# Load visited links from file
def load_visited_links():
    if os.path.exists(VISITED_LINKS_FILE):
        with open(VISITED_LINKS_FILE, "r") as file:
            return set(json.load(file))
    return set()

# Save visited links to file
def save_visited_links(visited_links):
    with open(VISITED_LINKS_FILE, "w") as file:
        json.dump(list(visited_links), file)

# Analyze the article (placeholder for actual implementation)
def analyze_article(title, text, publish_date, url, source_brand):
    # Replace with your actual analysis logic
    print(f"Analyzing article from {source_brand}: {title}")
    print(f"URL: {url}")
    print(f"Published on: {publish_date}")
    print(f"Content: {text[:500]}...")  # Print first 500 characters for brevity

# Process articles from a given source
def process_articles(source, visited_links):
    for article in source.articles:
        if article.url in visited_links:
            continue
        
        try:
            article.download()
            article.parse()
            
            # Add to visited links
            visited_links.add(article.url)
            
            # Call the analyze function
            analyze_article(
                title=article.title,
                text=article.text,
                publish_date=article.publish_date,
                url=article.url,
                source_brand=source.brand
            )
        except Exception as e:
            print(f"Failed to process article {article.url}: {e}")

# List of financial news sources
financial_news_sources = [
    'https://www.cnbc.com',            # CNBC
    'https://www.reuters.com/finance', # Reuters
    'https://www.bloomberg.com',       # Bloomberg
    'https://www.marketwatch.com',     # MarketWatch
    'https://www.ft.com/',             # Financial Times
    'https://www.investing.com/',      # Investing.com
    'https://www.forbes.com/finance/', # Forbes - Finance Section
    'https://www.theguardian.com/business', # The Guardian - Business Section
]

def main():
    visited_links = load_visited_links()
    print("Starting news scraping...")

    for source_url in financial_news_sources:
        print(f"Processing source: {source_url}")
        try:
            source = newspaper.build(source_url, memoize_articles=False)
            process_articles(source, visited_links)
        except Exception as e:
            print(f"Failed to process source {source_url}: {e}")

    save_visited_links(visited_links)
    print("News scraping complete.")

if __name__ == "__main__":
    main()
