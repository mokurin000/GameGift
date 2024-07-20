import asyncio
from datetime import datetime, timezone, timedelta

from playwright.async_api import async_playwright, BrowserContext, Page


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        with open("urls.txt", "r", encoding="utf-8") as url:
            urls = [line.strip() for line in url.readlines() if line.strip()]

        ctxs: list[BrowserContext] = []
        pages = []

        for url in urls:
            ctx = await browser.new_context()
            ctxs.append(ctx)
            page = await browser.new_page()
            await page.goto(url)
            pages.append(page)

        async def click_receive(page: Page):
            await page.reload()
            loc_receive = page.locator(
                "div.content.content1 li:first-child div.btn-box div.get-btn"
            )
            loc_confirm = page.locator(
                "div#modalTip div.modal-tip div.modal-content div.modal-btn-group div.modal-btn:nth-child(1)"
            )
            while True:
                # Receive rewards
                await loc_receive.click()
                await loc_confirm.click()

        tz = timezone(timedelta(hours=8))
        current_time = datetime.now(tz=tz)
        target_time = datetime.fromisoformat("2024-07-22T12:00:00+08:00")
        seconds_to_wait = max((target_time - current_time).total_seconds(), 0)
        print(f"Will wait {seconds_to_wait} seconds...")
        await asyncio.sleep(seconds_to_wait)

        try:
            await asyncio.gather(*(click_receive(page) for page in pages))
        finally:
            # Cleanup
            for ctx in ctxs:
                ctx.close()
            browser.close()


if __name__ == "__main__":
    asyncio.run(main())
