"""Get the professor links from CSRankings Website"""


import asyncio
import pprint

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def ascrape_playwright(url):
    """
    An asynchronous Python function that uses Playwright to scrape
    content from a given URL, extracting specified HTML tags and removing unwanted tags and unnecessary
    lines.
    """
    print("Started scraping...")
    results = ""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            await page.goto(url)

            page_source = await page.content()


            print("URLs scraped")
        except Exception as e:
            results = f"Error: {e}"
        await browser.close()
    return results


if __name__ == "__main__":
    url = "https://csrankings.org/#/index?ai&vision&mlmining&nlp&inforet&robotics&bio&ecom&world"

    async def scrape_playwright():
        results = await ascrape_playwright(url)
        print(results)

    pprint.pprint(asyncio.run(scrape_playwright()))