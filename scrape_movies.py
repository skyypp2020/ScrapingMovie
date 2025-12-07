import requests
from bs4 import BeautifulSoup
import csv
import re
import time

def scrape_movies():
    base_url = 'https://ssr1.scrape.center/page/{}'
    movies = []

    for page in range(1, 11):
        url = base_url.format(page)
        print(f"Scraping page {page}...")
        try:
            response = requests.get(url)
            response.raise_for_status()
            response.encoding = 'utf-8'
        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        
        items = soup.select('.el-card.item')
        if not items:
            print(f"No items found on page {page}")

        for item in items:
            movie = {}
            
            # Title
            name_tag = item.select_one('.name h2')
            movie['title'] = name_tag.get_text(strip=True) if name_tag else 'N/A'

            # Rating
            score_tag = item.select_one('.score')
            movie['score'] = score_tag.get_text(strip=True) if score_tag else 'N/A'

            # Categories
            categories = [span.get_text(strip=True) for span in item.select('.categories .category span')]
            movie['categories'] = '/'.join(categories)

            # Info: Country, Duration, Release Date
            info_divs = item.select('.info')
            if len(info_divs) >= 2:
                # First info div usually contains "Country / Duration"
                info_text_1 = info_divs[0].get_text(separator=' ', strip=True)
                parts = [p.strip() for p in info_text_1.split('/')]
                movie['country'] = parts[0] if len(parts) > 0 else 'N/A'
                movie['duration'] = parts[1] if len(parts) > 1 else 'N/A'

                # Second info div usually contains Release Date
                info_text_2 = info_divs[1].get_text(strip=True)
                # Extract date pattern YYYY-MM-DD
                match = re.search(r'\d{4}-\d{2}-\d{2}', info_text_2)
                movie['release_date'] = match.group(0) if match else info_text_2
            else:
                 movie['country'] = 'N/A'
                 movie['duration'] = 'N/A'
                 movie['release_date'] = 'N/A'

            movies.append(movie)
        
        # Be nice to the server
        time.sleep(1)

    # Save to CSV
    csv_file = 'movie.csv'
    headers = ['title', 'score', 'categories', 'country', 'duration', 'release_date']
    
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(movies)
        print(f"Successfully scraped {len(movies)} movies from 10 pages and saved to {csv_file}")
    except IOError as e:
        print(f"Error writing to CSV: {e}")

if __name__ == '__main__':
    scrape_movies()
