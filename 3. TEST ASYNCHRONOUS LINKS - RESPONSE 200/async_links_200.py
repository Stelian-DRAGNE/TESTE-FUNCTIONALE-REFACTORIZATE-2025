
from __future__ import annotations

import argparse
import asyncio
import csv
import logging
import os
import sys
import time
import unittest
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Iterable
from urllib.parse import urlsplit, urlunsplit

import aiohttp



def setup_logging(quiet: bool = False) -> None:

    level = logging.WARNING if quiet else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler()],
    )


DEFAULT_TIMEOUT = 10
DEFAULT_UA = "AsyncLinkChecker/1.2"
REDIRECT_STATUSES = {301, 302, 303, 307, 308}


@dataclass(frozen=True)
class CheckerConfig:

    concurrency: int = 20
    timeout: int = DEFAULT_TIMEOUT
    retries: int = 2
    user_agent: str = DEFAULT_UA
    allow_redirects: bool = True
    verify_ssl: bool = True


def _is_http_url(u: str) -> bool:
    try:
        p = urlsplit(u)
    except Exception:
        return False
    return p.scheme in ("http", "https") and bool(p.netloc)


def _normalize_url(u: str) -> str:

    u = (u or "").strip()
    if not _is_http_url(u):
        return u
    p = urlsplit(u)
    return urlunsplit((p.scheme.lower(), p.netloc, p.path or "/", p.query, ""))


def _status_category(code: int) -> str:

    if code == 200:
        return "OK"
    if code in REDIRECT_STATUSES:
        return "REDIRECT"
    if 400 <= code <= 499:
        return "CLIENT_ERROR"
    if 500 <= code <= 599:
        return "SERVER_ERROR"
    return "ERROR"


def _exp_backoff(attempt: int) -> float:

    base = 0.5 * (2 ** max(0, attempt - 1))
    return base + (0.25 * (attempt + 1))


class AsyncLinkChecker:

    def __init__(self, csv_file: str, max_links: Optional[int] = None, config: CheckerConfig = CheckerConfig()) -> None:
        self.csv_file = csv_file
        self.max_links = max_links
        self.cfg = config
        self.links: List[str] = []
        self._session: Optional[aiohttp.ClientSession] = None
        self._sem = asyncio.Semaphore(self.cfg.concurrency)


    def load_links(self) -> List[str]:

        if not os.path.exists(self.csv_file):
            logging.error("Fișierul '%s' nu există.", self.csv_file)
            return []

        try:
            with open(self.csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames:
                    logging.error("Fișierul '%s' nu are antet valid.", self.csv_file)
                    return []

                url_col = next(
                    (c for c in reader.fieldnames if c and c.strip().lower() in ("url", "link")),
                    reader.fieldnames[0],
                )
                if url_col not in ("url", "link"):
                    logging.warning("Coloana nu e 'url' sau 'link', folosim '%s'", url_col)

                raw_links = [(row.get(url_col) or "").strip() for row in reader]
                self.links = [u for u in (_normalize_url(x) for x in raw_links) if _is_http_url(u)]

            if self.max_links:
                self.links = self.links[: self.max_links]

            logging.info("Am încărcat %d link-uri din '%s'", len(self.links), self.csv_file)
            return self.links
        except OSError as e:
            logging.error("Eroare la citirea fișierului '%s': %s", self.csv_file, e)
            return []


    async def __aenter__(self):
        connector = aiohttp.TCPConnector(
            limit=self.cfg.concurrency,
            enable_cleanup_closed=True,
            ttl_dns_cache=300,
            ssl=None if self.cfg.verify_ssl else False,
        )
        timeout = aiohttp.ClientTimeout(total=self.cfg.timeout)
        headers = {"User-Agent": self.cfg.user_agent, "Accept": "*/*"}
        self._session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=headers,
            raise_for_status=False,
            trust_env=True,
        )
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._session:
            await self._session.close()
            self._session = None


    async def _request_with_fallback(self, url: str) -> int:
        assert self._session is not None
        try:
            async with self._session.head(url, allow_redirects=self.cfg.allow_redirects) as resp:
                if resp.status not in (405, 403):
                    return resp.status
        except Exception as e:
            logging.debug("HEAD a eșuat pentru %s: %s", url, e)

        async with self._session.get(url, allow_redirects=self.cfg.allow_redirects) as resp:
            return resp.status

    async def fetch(self, url: str) -> Tuple[str, int, str]:
        async with self._sem:
            for attempt in range(self.cfg.retries + 1):
                try:
                    status = await self._request_with_fallback(url)
                    category = _status_category(status)
                    if category != "ERROR" or attempt == self.cfg.retries:
                        return url, status, category
                except Exception as e:
                    logging.warning("Eroare la %s (try %d/%d): %s", url, attempt + 1, self.cfg.retries + 1, e)
                await asyncio.sleep(_exp_backoff(attempt))
            return url, -1, "ERROR"

    async def scrape_urls(self, urls: Optional[Iterable[str]] = None) -> List[Tuple[str, int, str]]:
        urls_to_check = list(urls or self.links)
        if not urls_to_check:
            logging.warning("Lista de link-uri este goală.")
            return []

        if self._session is None:
            async with self:
                return await self.scrape_urls(urls_to_check)

        return await asyncio.gather(*(self.fetch(u) for u in urls_to_check))


    @staticmethod
    def summarize_results(results: List[Tuple[str, int, str]], max_examples: int = 5) -> Dict[str, List]:

        ok = [u for u, status, _ in results if status == 200]
        not_ok = [(u, status) for u, status, _ in results if status != 200]

        logging.info("OK: %d, Probleme: %d", len(ok), len(not_ok))
        if not_ok:
            logging.warning("Primele %d erori:", min(max_examples, len(not_ok)))
            for url, status in not_ok[:max_examples]:
                logging.warning(" %s -> %s", status, url)

        return {"ok": ok, "not_ok": not_ok}

    @staticmethod
    def write_results_csv(filename: str, results: List[Tuple[str, int, str]], include_category: bool = False) -> None:

        if not results:
            logging.warning("Nu există rezultate de scris.")
            return
        try:
            os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
            with open(filename, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                header = ["url", "status"] + (["category"] if include_category else [])
                writer.writerow(header)
                for url, status, category in results:
                    row = [url, status] + ([category] if include_category else [])
                    writer.writerow(row)
            logging.info("Rezultatele au fost scrise în '%s'", filename)
        except OSError as e:
            logging.error("Eroare la scrierea fișierului '%s': %s", filename, e)


class TestAsyncLinkChecker(unittest.TestCase):
    def setUp(self) -> None:
        self.checker = AsyncLinkChecker("dummy.csv")

    def test_summarize_results(self) -> None:
        results = [("http://ok.com", 200, "OK"), ("http://bad.com", 404, "CLIENT_ERROR")]
        summary = self.checker.summarize_results(results)
        self.assertEqual(summary["ok"], ["http://ok.com"])
        self.assertIn(("http://bad.com", 404), summary["not_ok"])


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Async Link Checker")
    parser.add_argument("--csv", type=str, default="async_links.csv", help="Fișierul CSV cu link-uri")
    parser.add_argument("--output", type=str, default="status_links.csv", help="CSV de ieșire")
    parser.add_argument("--max-links", type=int, help="Limitează numărul de link-uri")
    parser.add_argument("--workers", type=int, default=20, help="Nr. request-uri concurente")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Timeout per request")
    parser.add_argument("--retries", type=int, default=2, help="Nr. încercări per request")
    parser.add_argument("--quiet", action="store_true", help="Doar WARN/ERROR")
    parser.add_argument("--include-category", action="store_true", help="Include coloana category în CSV")
    parser.add_argument("--test", action="store_true", help="Rulează testele integrate")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:

    args = parse_args(argv)
    setup_logging(args.quiet)

    if args.test:
        unittest.main(argv=[sys.argv[0]])
        return

    cfg = CheckerConfig(
        concurrency=max(1, args.workers),
        timeout=max(1, args.timeout),
        retries=max(0, args.retries),
    )
    checker = AsyncLinkChecker(args.csv, max_links=args.max_links, config=cfg)
    checker.load_links()

    if not checker.links:
        logging.error("Nu există link-uri de verificat.")
        sys.exit(1)

    start = time.time()

    async def run_check() -> List[Tuple[str, int, str]]:
        async with checker:
            return await checker.scrape_urls()

    results = asyncio.run(run_check())
    logging.info("Timp execuție: %.2f sec", time.time() - start)

    checker.summarize_results(results)
    checker.write_results_csv(args.output, results, include_category=args.include_category)


if __name__ == "__main__":
    main()
