
from __future__ import annotations

import asyncio
import csv
import logging
import os
import random
import sys
import time
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
from urllib.parse import urlsplit, urlunsplit

import aiohttp



def setup_logging(quiet: bool = False) -> None:

    level = logging.WARNING if quiet else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler()],
    )


@dataclass(frozen=True)
class CheckerConfig:
    concurrency: int = 20
    timeout: int = 10
    retries: int = 2
    user_agent: str = "AsyncLinkChecker/1.3"
    allow_redirects: bool = True
    verify_ssl: bool = True


def normalize_url(u: str) -> str:

    try:
        u = (u or "").strip()
        p = urlsplit(u)
        if not p.scheme or not p.netloc:
            return u
        return urlunsplit((p.scheme.lower(), p.netloc, p.path or "/", p.query, ""))
    except Exception:
        return u


def status_category(code: int) -> str:

    if code == 200:
        return "OK"
    if code == 404:
        return "NOT_FOUND"
    if code in (301, 302, 303, 307, 308):
        return "REDIRECT"
    if 400 <= code <= 499:
        return "CLIENT_ERROR"
    if 500 <= code <= 599:
        return "SERVER_ERROR"
    return "ERROR"


def backoff(attempt: int) -> float:

    return min(5, (2 ** attempt) + random.uniform(0, 0.5))


class AsyncLinkChecker:

    def __init__(self, csv_file: str, config: CheckerConfig = CheckerConfig(), max_links: Optional[int] = None) -> None:
        self.csv_file = csv_file
        self.cfg = config
        self.max_links = max_links
        self.links: List[str] = []
        self._session: Optional[aiohttp.ClientSession] = None
        self._sem = asyncio.Semaphore(self.cfg.concurrency)

    async def __aenter__(self):
        connector = aiohttp.TCPConnector(
            limit=self.cfg.concurrency,
            ttl_dns_cache=300,
            ssl=self.cfg.verify_ssl,
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
                    (c for c in reader.fieldnames if c.strip().lower() in ("url", "link")),
                    reader.fieldnames[0],
                )
                if url_col not in ("url", "link"):
                    logging.warning("Coloana link-urilor nu e 'url' sau 'link', folosim '%s'", url_col)

                self.links = [normalize_url(row[url_col]) for row in reader if row.get(url_col)]

            if self.max_links:
                self.links = self.links[: self.max_links]

            logging.info("Am încărcat %d link-uri din '%s'", len(self.links), self.csv_file)
            return self.links
        except OSError as e:
            logging.error("Eroare la citirea fișierului '%s': %s", self.csv_file, e)
            return []

    async def _request(self, url: str) -> int:

        assert self._session is not None
        try:
            async with self._session.head(url, allow_redirects=self.cfg.allow_redirects) as resp:
                if resp.status not in (405, 403):
                    return resp.status
        except Exception:
            pass
        async with self._session.get(url, allow_redirects=self.cfg.allow_redirects) as resp:
            return resp.status

    async def fetch(self, url: str) -> Tuple[str, int, str]:

        async with self._sem:
            for attempt in range(self.cfg.retries + 1):
                try:
                    status = await self._request(url)
                    return url, status, status_category(status)
                except Exception as e:
                    logging.warning("Eroare la %s (try %d/%d): %s", url, attempt + 1, self.cfg.retries + 1, e)
                    await asyncio.sleep(backoff(attempt))
            return url, -1, "ERROR"

    async def scrape_urls(self, urls: Optional[List[str]] = None) -> List[Tuple[str, int, str]]:

        urls_to_check = urls or self.links
        if not urls_to_check:
            logging.warning("Lista de link-uri este goală.")
            return []

        if not self._session:
            async with self:
                return await self.scrape_urls(urls_to_check)

        tasks = [self.fetch(u) for u in urls_to_check]
        return await asyncio.gather(*tasks)

    @staticmethod
    def summarize_results(results: List[Tuple[str, int, str]]) -> Dict[str, int]:

        total = len(results)
        ok = sum(1 for _, _, c in results if c == "OK")
        not_found = sum(1 for _, _, c in results if c == "NOT_FOUND")
        redirects = sum(1 for _, _, c in results if c == "REDIRECT")
        errors = total - ok - not_found - redirects

        logging.info("=== Rezumat ===")
        logging.info("Total: %d | OK: %d | NotFound: %d | Redirects: %d | Erori: %d",
                        total, ok, not_found, redirects, errors)
        return {"total": total, "ok": ok, "not_found": not_found, "redirects": redirects, "errors": errors}

    @staticmethod
    def write_results_csv(filename: str, results: List[Tuple[str, int, str]]) -> None:

        if not results:
            logging.warning("Nu există rezultate de scris.")
            return
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
        try:
            with open(filename, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["url", "status", "category"])
                writer.writerows(results)
            logging.info("Rezultatele au fost scrise în '%s'", filename)
        except OSError as e:
            logging.error("Eroare la scrierea fișierului '%s': %s", filename, e)


if __name__ == "__main__":
    setup_logging()
    csv_file = "async_links.csv"
    checker = AsyncLinkChecker(csv_file, CheckerConfig(concurrency=20, timeout=10, retries=2), max_links=100)

    checker.load_links()
    if not checker.links:
        logging.error("Nu există link-uri de verificat. Verifică fișierul CSV și coloana corespunzătoare.")
        sys.exit(1)

    start = time.time()

    async def run_check():
        async with checker:
            return await checker.scrape_urls()

    results = asyncio.run(run_check())
    logging.info("Verificarea s-a realizat în %.2f secunde.", time.time() - start)

    checker.summarize_results(results)
    checker.write_results_csv("async_links_status.csv", results)
