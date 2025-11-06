import os
import json
import sqlite3
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count

DB_FILE = "items.db"

def init_db():
    """Create the database and table if not exists"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            image_url TEXT,
            cost TEXT,
            url TEXT
        )
    """)
    conn.commit()
    conn.close()

def scrape_page(html_file):
    """Scrape auction items from a single page"""
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')

    items = []
    item_divs = soup.find_all('div', class_=lambda x: x and 'flex flex-col justify-between' in x and 'rounded-xl' in x)
    for div in item_divs:
        name_tag = div.find('h4')
        img_tag = div.find('img')
        bid_tag = div.find('span', class_='mb-1')
        url = div.find('a')

        name = name_tag.get_text(strip=True) if name_tag else None
        image_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else None
        url = url['href'] if url and url.has_attr('href') else None

        cost = None
        if bid_tag:
            text = bid_tag.get_text(strip=True)
            cost = text.replace('CURRENT BID: $', '').replace('<!-- -->', '').strip()

        items.append((name, image_url, cost, url))
    return items

def save_to_db(items):
    """Insert scraped items into the database"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.executemany("INSERT INTO items (name, image_url, cost, url) VALUES (?, ?, ?, ?)", items)
    conn.commit()
    conn.close()

def main():
    init_db()

    pagecache_dir = 'pagecache'
    html_files = [
        os.path.join(pagecache_dir, f)
        for f in sorted(os.listdir(pagecache_dir))
        if f.endswith('.html')
    ]

    print(f"Processing {len(html_files)} files using {cpu_count()} cores...")

    all_items = []
    with Pool(cpu_count()) as pool:
        for result in pool.imap_unordered(scrape_page, html_files):
            all_items.extend(result)

    save_to_db(all_items)

    print(f"Scraped {len(all_items)} items and saved to {DB_FILE}")

if __name__ == "__main__":
    main()
