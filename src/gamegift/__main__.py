import asyncio
from datetime import datetime, timezone, timedelta, date, time

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
            loc = page.locator(
                "div.content.content1 li:first-child div.btn-box div.get-btn"
            )
            # Receive rewards
            await loc.click()

        tz = timezone(timedelta(hours=8))
        current_time = datetime.now(tz=tz)
        target_time = datetime.combine(
            date=date.today(), time=time.fromisoformat("20:00:00"), tzinfo=tz
        )
        seconds_to_wait = max((target_time - current_time).total_seconds() - 15, 0)
        print(f"Will wait {seconds_to_wait} secs...")
        await asyncio.sleep(seconds_to_wait)

        try:
            while True:
                await asyncio.gather(*(click_receive(page) for page in pages))
                await asyncio.sleep(0.5)
        finally:
            # Cleanup
            for ctx in ctxs:
                ctx.close()
            browser.close()


if __name__ == "__main__":
    asyncio.run(main())
