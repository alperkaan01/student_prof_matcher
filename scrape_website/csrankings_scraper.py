"""Get the professor links from CSRankings Website"""


import asyncio
import pprint

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from professor import Professor

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

        url_dict = {}  #dict of dictionaries

        try:
            page = await browser.new_page()
            await page.goto(url)

            page_source = await page.content()

            # Use BeautifulSoup to parse HTML
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Convert the XPath to a CSS selector
            element = soup.select_one('body > div:nth-of-type(5) > form > div > div:nth-of-type(2) > div:nth-of-type(2) > div > div > table > tbody')
            
            print(type(element))

        
        except Exception as e:
            results = f"Error: {e}"
        await browser.close()
    
    return results #change this









if __name__ == "__main__":
    url = "https://csrankings.org/#/index?ai&vision&mlmining&nlp&inforet&robotics&bio&ecom&world"

    async def scrape_playwright():
        results = await ascrape_playwright(url)
        print(results)

    pprint.pprint(asyncio.run(scrape_playwright()))