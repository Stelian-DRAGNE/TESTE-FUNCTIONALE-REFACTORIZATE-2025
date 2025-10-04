
from __future__ import annotations

import argparse
import csv
import logging
import os
import sys
import tempfile
import unittest
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup



TIMEOUT: int = 10
DEFAULT_USER_AGENT: str = "SitemapParser/1.0"
DEFAULT_WORKERS: int = 20

logger = logging.getLogger("sitemap_parser")
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def configure_requests_session(user_agent: Optional[str] = None) -> requests.Session:

    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=3)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({"User-Agent": user_agent or DEFAULT_USER_AGENT})
    return session


@dataclass
class SitemapParser:

    root_sitemap: str
    max_workers: int = DEFAULT_WORKERS
    session: requests.Session = field(default_factory=configure_requests_session)
    all_links: List[str] = field(default_factory=list)

    def fetch_links_from_sitemap(self, sitemap_url: str) -> List[str]:

        try:
            resp = self.session.get(sitemap_url, timeout=TIMEOUT)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, "xml")
            links = [loc.text.strip() for loc in soup.find_all("loc") if loc.text.strip()]
            logger.info("✔ %d link-uri extrase din %s", len(links), sitemap_url)
            return links
        except requests.RequestException as e:
            logger.error("✖ Eroare la descărcarea sitemap-ului %s: %s", sitemap_url, e)
            return []

    def get_all_links(self) -> List[str]:

        self.all_links.clear()
        root_links = self.fetch_links_from_sitemap(self.root_sitemap)

        if not root_links:
            logger.warning("Nu s-au găsit sitemap-uri secundare în root.")
            return []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_sitemap = {
                executor.submit(self.fetch_links_from_sitemap, url): url
                for url in root_links
            }
            for future in as_completed(future_to_sitemap):
                sitemap_url = future_to_sitemap[future]
                try:
                    links = future.result()
                    self.all_links.extend(links)
                except Exception as e:
                    logger.exception("Eroare la procesarea sitemap-ului %s: %s", sitemap_url, e)

        logger.info("✔ Total link-uri găsite: %d", len(self.all_links))
        return self.all_links

    @staticmethod
    def filter_links(links: List[str], keyword: str) -> Dict[str, List[str]]:

        keyword = keyword.strip()
        if not keyword:
            logger.warning("Keyword gol – toate linkurile vor fi clasificate drept 'other'")
            return {"matching": [], "others": links}

        matching = [l for l in links if keyword in l]
        others = [l for l in links if keyword not in l]
        logger.info("✔ %d link-uri conțin '%s', %d altele", len(matching), keyword, len(others))
        return {"matching": matching, "others": others}

    @staticmethod
    def write_links_csv(filename: str, categorized_links: Dict[str, List[str]]) -> None:

        if not categorized_links:
            logger.warning("✖ Nu există link-uri de scris în %s", filename)
            return

        try:
            os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
            with open(filename, "w", encoding="utf-8", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["type", "url"])
                for link in categorized_links.get("matching", []):
                    writer.writerow(["cdn", link])
                for link in categorized_links.get("others", []):
                    writer.writerow(["other", link])

            total = sum(len(v) for v in categorized_links.values())
            logger.info("✔ Scrise %d link-uri în %s", total, filename)
        except OSError as e:
            logger.error("✖ Eroare la scrierea fișierului %s: %s", filename, e)


class TestSitemapParser(unittest.TestCase):

    def test_filter_links(self):
        links = ["https://cdn.example.com/img1", "https://site.com/page"]
        categorized = SitemapParser.filter_links(links, "cdn")
        self.assertEqual(len(categorized["matching"]), 1)
        self.assertEqual(len(categorized["others"]), 1)

    def test_filter_links_empty_keyword(self):
        links = ["https://cdn.example.com/img1"]
        categorized = SitemapParser.filter_links(links, "")
        self.assertEqual(len(categorized["matching"]), 0)
        self.assertEqual(len(categorized["others"]), 1)

    def test_write_links_csv(self):
        categorized = {
            "matching": ["https://cdn.example.com/img1"],
            "others": ["https://site.com/page"],
        }
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmpfile:
            filename = tmpfile.name

        try:
            SitemapParser.write_links_csv(filename, categorized)
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("cdn", content)
            self.assertIn("other", content)
        finally:
            os.remove(filename)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="Sitemap Parser Tool")
    parser.add_argument(
        "--sitemap",
        type=str,
        default="https://www.mosionroata.ro/sitemap.xml",
        help="URL-ul sitemap-ului root",
    )
    parser.add_argument(
        "--keyword",
        type=str,
        default="gomagcdn",
        help="Cuvântul cheie pentru filtrare link-uri",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="sync_links.csv",
        help="Fișierul CSV de ieșire",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help="Număr de thread-uri pentru descărcare concurrentă",
    )
    parser.add_argument("--test", action="store_true", help="Rulează testele integrate")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)

    if args.test:
        unittest.main(argv=[sys.argv[0]])
        return

    parser_obj = SitemapParser(args.sitemap, max_workers=args.workers)
    all_links = parser_obj.get_all_links()

    if not all_links:
        logger.error("✖ Nu s-au găsit linkuri. Ieșim cu cod 1.")
        sys.exit(1)

    categorized = parser_obj.filter_links(all_links, args.keyword)
    parser_obj.write_links_csv(args.output, categorized)


if __name__ == "__main__":
    main()
