import requests
import time
import multiprocessing as mp
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import os
locationid = os.getenv("locationid", "0")
pages = os.getenv("pages", "0")
def fetch_page(page_num):
    time.sleep(0.1)  # Still be polite
    print(f"Fetching page {page_num}...")
    try:
        response = requests.get(f"https://www.bidfta.com/items?pageId={page_num}&locations={locationid}")
        Path("pagecache").mkdir(exist_ok=True)
        with open(f"pagecache/page_{page_num}.html", "w", encoding="utf-8") as file:
            file.write(response.text)
        return f"Successfully fetched page {page_num}"
    except Exception as e:
        return f"Error fetching page {page_num}: {str(e)}"

if __name__ == '__main__':
    # Create a pool of workers (using 75% of available CPU cores)
    num_cores = max(1, int(mp.cpu_count() * 0.75))
    print(f"Using {num_cores} processes")
    
    # Create the process pool
    with mp.Pool(num_cores) as pool:
        # Map the fetch_page function to all page numbers
        results = pool.map(fetch_page, range(1, int(pages) + 1))
    
    # Print any errors that occurred
    for result in results:
        if "Error" in result:
            print(result)