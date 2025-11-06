# Bidfta scraper

Small scripts to scrape Bidfta (an Amazon-return reseller) and extract auction data into a SQLite database.

This repository contains simple tools to cache auction pages and then process those cached pages to extract structured auction information.

## Contents

- `scrape.py` — crawl Bidfta auction listing pages and cache raw HTML pages locally.
- `prosess.py` — parse the cached files and extract auction metadata into a SQLite database.
- `items.db` — the output db of all the items

> Note: The filename `prosess.py` is intentionally named that way in this repo. Use that exact filename when running the processing step.

## Prerequisites

- Python 3.8+ installed
- Recommended: create and use a virtual environment

There may not be a `requirements.txt` in the repo. If you add one, install dependencies like this (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If no `requirements.txt` is provided, the scripts should work with the standard library plus widely-used libraries such as `requests` and `beautifulsoup4` if needed — add them to `requirements.txt` if you depend on them.

## Quick start (PowerShell)

1. Cache auction pages:

```powershell
python scrape.py
```

2. Process the cached pages into the SQLite DB:

```powershell
python prosess.py
```

The scripts will create a SQLite database file in the workspace (look for files with `.db` or `.sqlite` extension). If you want a different output file name, open `prosess.py` and check where the DB connection is created.

## Polite scraping and robots.txt

Bidfta's robots.txt allows crawling of item lists and past auctions, but be polite:

- Respect `robots.txt` and site terms of service.
- Add delays (e.g., 1–3 seconds) between requests to avoid burdening the server.
- Avoid high concurrency and bulk re-requests.

## Troubleshooting

- If pages are not being cached, check network access and whether the script is blocked by headers or anti-bot measures.
- If parsing fails, examine one of the cached HTML files in `items/` to confirm the structure hasn't changed.
- If the DB file is not created, open `prosess.py` and check for the output path or any exceptions the script prints.

## TODO / Improvements

- Add a `requirements.txt` with pinned dependencies.
- Add a small example of expected DB schema or sample output JSON/CSV.
- Add unit tests for the parsing logic in `prosess.py`.

## Contributing

If you'd like to improve this project, please:

- Open issues describing missing features or bugs.
- Send a pull request with a focused change (for code changes include tests).

## License

No license is specified in this repository. Add a `LICENSE` file if you want to set the project license.

## Contact

If you want help improving the scripts or adding tests, tell me what you want changed (for example: add `requirements.txt`, show example DB schema, add rate-limiting knobs, or fix a parser). 
