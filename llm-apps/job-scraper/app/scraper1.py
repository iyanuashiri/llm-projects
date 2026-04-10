from typing import List

from playwright.async_api import Page, async_playwright


async def scrape_webpage(url: str, is_paginated: bool = False) -> List[str]:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=0)

        if is_paginated:
            documents = await _scrape_paginated(page)
        else:
            documents = [await page.content()]

        await browser.close()
        return documents


async def _scrape_paginated(page: Page) -> List[str]:
    documents = []
    page_number = 1
    while True:
        try:
            documents.append(await page.content())
            await page.get_by_role("button", name=str(page_number + 1)).click()
            await page.wait_for_load_state(state="domcontentloaded", timeout=0)
            page_number += 1
        except Exception as e:
            print(f"Pagination stopped at page {page_number}: {e}")
            break
    return documents
