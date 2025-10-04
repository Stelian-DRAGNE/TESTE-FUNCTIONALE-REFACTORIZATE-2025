
from __future__ import annotations

import argparse
import logging
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup



logger = logging.getLogger("sitemap_checker")
handler = logging.StreamHandler()
formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


TIMEOUT: int = 10
DEFAULT_USER_AGENT: str = "SitemapChecker/1.0"
DEFAULT_WORKERS: int = 20


def configure_requests_session(user_agent: Optional[str] = None) -> requests.Session:

    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=3)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({"User-Agent": user_agent or DEFAULT_USER_AGENT})
    return session


@dataclass
class SitemapChecker:

    sitemaps: List[str]
    max_workers: int = DEFAULT_WORKERS
    session: requests.Session = field(default_factory=configure_requests_session)
    results: Dict[str, Dict[str, bool]] = field(default_factory=dict)

    def fetch_urls(self, sitemap_url: str) -> List[str]:

        try:
            resp = self.session.get(sitemap_url, timeout=TIMEOUT)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, "xml")
            urls = [loc.text.strip() for loc in soup.find_all("loc") if loc.text.strip()]
            logger.info("✔ %d URL-uri extrase din %s", len(urls), sitemap_url)
            return urls
        except requests.RequestException as e:
            logger.error("✖ Eroare la descărcarea sitemap-ului %s: %s", sitemap_url, e)
            return []

    def is_broken(self, url: str) -> bool:

        try:
            response = self.session.head(url, allow_redirects=True, timeout=TIMEOUT)
            if response.status_code == 405:
                response = self.session.get(url, allow_redirects=True, timeout=TIMEOUT)

            if 400 <= response.status_code < 600:
                logger.warning("[%s] Link nefuncțional: %s", response.status_code, url)
                return True
            return False
        except requests.RequestException as e:
            logger.error("Eroare la verificarea %s: %s", url, e)
            return True

    def check_urls_concurrent(self, urls: List[str]) -> Dict[str, bool]:

        results: Dict[str, bool] = {}
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {executor.submit(self.is_broken, url): url for url in urls}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    results[url] = future.result()
                except Exception as e:
                    logger.exception("Eroare în thread pentru %s: %s", url, e)
                    results[url] = True
        return results

    def process_sitemaps(self) -> None:

        for sitemap in self.sitemaps:
            logger.info("=== Procesare sitemap: %s ===", sitemap)
            urls = self.fetch_urls(sitemap)
            if not urls:
                self.results[sitemap] = {}
                continue

            broken_status = self.check_urls_concurrent(urls)
            self.results[sitemap] = broken_status

            broken_links = [u for u, is_broken in broken_status.items() if is_broken]
            if broken_links:
                logger.info("✖ %d linkuri nefuncționale în %s", len(broken_links), sitemap)
            else:
                logger.info("✔ Toate linkurile sunt funcționale în %s", sitemap)

    def get_broken_links(self) -> Dict[str, List[str]]:

        return {
            sitemap: [url for url, broken in urls.items() if broken]
            for sitemap, urls in self.results.items()
        }

    def get_all_links(self) -> Dict[str, List[str]]:

        return {sitemap: list(urls.keys()) for sitemap, urls in self.results.items()}


class TestSitemapChecker(unittest.TestCase):

    def setUp(self):
        self.checker = SitemapChecker([])

    def test_broken_links_summary(self):
        self.checker.results = {"sitemap.xml": {"http://ok.com": False, "http://bad.com": True}}
        broken = self.checker.get_broken_links()
        self.assertIn("http://bad.com", broken["sitemap.xml"])
        self.assertNotIn("http://ok.com", broken["sitemap.xml"])

    def test_all_links_summary(self):
        self.checker.results = {"sitemap.xml": {"http://ok.com": False}}
        all_links = self.checker.get_all_links()
        self.assertEqual(all_links["sitemap.xml"], ["http://ok.com"])


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="Sitemap Checker")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help="Numărul maxim de thread-uri")
    parser.add_argument(
        "--sitemap",
        nargs="+",
        default=[
            "https://www.mosionroata.ro/sitemap.xml",
            "https://www.olx.ro/sitemap.xml",
            "https://www.raijucarii.ro/sitemap.xml",
            "https://tazz.ro/sitemap.xml",
            "https://www.google.ro/sitemap.xml",
        ],
        help="Lista de sitemap-uri de procesat",
    )
    parser.add_argument("--test", action="store_true", help="Rulează testele integrate")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)

    if args.test:
        unittest.main(argv=[sys.argv[0]])
        return

    checker = SitemapChecker(args.sitemap, max_workers=args.workers)
    checker.process_sitemaps()

    broken = checker.get_broken_links()
    for sitemap, links in broken.items():
        if links:
            logger.info("✖ %d linkuri nefuncționale în %s", len(links), sitemap)


if __name__ == "__main__":
    main()
