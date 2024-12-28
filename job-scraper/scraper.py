from typing import List

from playwright.async_api import async_playwright, Page


class WebScraper:
    def __init__(self, url: str, is_paginated: bool = False):
        self.url = url
        self.is_paginated = is_paginated

    async def scrape(self) -> List[str]:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(
                headless=True,  # Ensure headless mode
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage'
                ]
            )
            page = await browser.new_page()
            await page.goto(self.url, wait_until="domcontentloaded", timeout=0)

            if self.is_paginated:
                documents = await self._scrape_paginated(page)
            else:
                documents = [await self._scrape_single_page(page)]

            await browser.close()
            return documents

    async def _scrape_single_page(self, page: Page) -> str:
        return await page.content()

    async def _scrape_paginated(self, page: Page) -> List[str]:
        documents = []
        page_number = 1

        while True:
            try:
                document = await self._scrape_single_page(page)
                documents.append(document)
                # print(f"Scraped page {page_number}")

                next_button = await page.get_by_role("button", name=f"{page_number + 1}").click()
                
                await page.wait_for_load_state(state="domcontentloaded", timeout=0)

                page_number += 1
                # await asyncio.sleep(2)  # To avoid overwhelming the server
            except Exception as e:
                print(f"Error on page {page_number}: {str(e)}")
                break

        return documents

