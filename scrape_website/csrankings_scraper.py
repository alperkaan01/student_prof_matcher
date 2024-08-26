"""Get the professor links from CSRankings Website"""

import asyncio
import pprint

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def ascrape_playwright(url):
    """
    An asynchronous Python function that uses Playwright to scrape
    content from a given URL, extracting only the direct tr elements within a specific tbody.
    """
    print("Started scraping...")
    results = []
    university_database = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        try:
            page = await browser.new_page()
            await page.goto(url)
            
            # Wait for the table to load
            await page.wait_for_selector("table tbody")

            # Use XPath to locate the specific tbody
            tbody_locator = page.locator('//html/body/div[5]/form/div/div[2]/div[2]/div/div/table/tbody')

            # Get the inner HTML of the specific tbody
            tbody_content = await tbody_locator.inner_html()

            # Use BeautifulSoup to parse the tbody HTML content
            soup = BeautifulSoup(tbody_content, 'html.parser')

            # Extract all direct table rows (tr) from the specific tbody
            rows = soup.find_all('tr', recursive=False)
            
            
            for i in range(0, len(rows), 3):
                # Process every third row
                row = rows[i]

                # Find the <span> tag that contains the university name
                university_span = row.find_all('span', onclick=lambda x: x and 'csr.toggleFaculty' in x)
                
                if len(university_span) > 1:
                    university_name = university_span[1].get_text(strip=True)
                    
                    if(university_name not in university_database):
                        university_database[university_name] = []
                

            for i in range(len(rows)):
                print(i)
        
            



        except Exception as e:
            results = f"Error: {e}"
        
        await browser.close()

    return results

if __name__ == "__main__":
    url = "https://csrankings.org/#/index?ai&vision&mlmining&nlp&inforet&robotics&bio&ecom&world"

    async def scrape_playwright():
        results = await ascrape_playwright(url)
        pprint.pprint(results)  # Use pprint for better readability of the list of rows

    asyncio.run(scrape_playwright())