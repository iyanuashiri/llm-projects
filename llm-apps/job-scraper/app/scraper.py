import asyncio
import sys
from typing import List
from concurrent.futures import ThreadPoolExecutor

from playwright.sync_api import sync_playwright


def _run_scrape_sync(url: str, is_paginated: bool) -> List[str]:
    """Run playwright synchronously in a thread to avoid Windows event loop issues."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)

        if is_paginated:
            documents = _scrape_paginated_sync(page)
        else:
            documents = [page.content()]

        browser.close()
        return documents


def _scrape_paginated_sync(page) -> List[str]:
    documents = []
    page_number = 1

    while True:
        try:
            documents.append(page.content())
            page.get_by_role("button", name=str(page_number + 1)).click()
            page.wait_for_load_state(state="domcontentloaded", timeout=30000)
            page_number += 1
        except Exception as e:
            print(f"Pagination stopped at page {page_number}: {e}")
            break

    return documents


_executor = ThreadPoolExecutor(max_workers=4)


class WebScraper:
    def __init__(self, url: str, is_paginated: bool = False):
        self.url = url
        self.is_paginated = is_paginated

    async def scrape(self) -> List[str]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            _executor,
            _run_scrape_sync,
            self.url,
            self.is_paginated
        )

