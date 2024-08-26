"""Get the professor links from CSRankings Website"""

import asyncio
import pprint

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from professor import Professor

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
                    print(university_name)

                    if(university_name not in university_database):
                        university_database[university_name] = []
                

                if i + 2 < len(rows):  # Check if the next row exists
                    row_professors = rows[i + 2]
                    print(f"Fetching the professor information for {university_name}")
                    
                    # Parse the row with BeautifulSoup
                    table_finder = BeautifulSoup(str(row_professors), 'html.parser')
                    
                    # Find all <tbody> elements within this row, if present
                    professor_tbody = table_finder.find("tbody")

                    if professor_tbody:
                        # Extract all <tr> elements from this <tbody>
                        professor_rows = professor_tbody.find_all("tr")
                        for i in range(0, len(professor_rows), 2):
                            # Process each professor row as needed
                            row = professor_rows[i]
                            
                                                        # Extract the professor's name
                            name_tag = row.find('a', title=True)
                            professor_name = name_tag.get_text(strip=True) if name_tag else "Name not found"

                            # Extract the URL of the professor's website
                            professor_url = name_tag['href'] if name_tag else "URL not found"

                            # Extract the AI area
                            ai_area_tag = row.find('span', class_='ai-area')
                            ai_area = ai_area_tag.get_text(strip=True) if ai_area_tag else "AI area not found"

                            # Print or store the extracted information
                            # print(f"Professor Name: {professor_name}")
                            # print(f"Professor URL: {professor_url}")
                            # print(f"AI Area: {ai_area}")

                            prof = Professor(name=professor_name, area=ai_area, url=professor_url)

                            university_database[university_name].append(prof)
            
            

            results = university_database

        except Exception as e:
            results = f"Error: {e}"
        
        await browser.close()

    return results

if __name__ == "__main__":
    url = "https://csrankings.org/#/index?ai&vision&mlmining&nlp&inforet&robotics&bio&ecom&world"

    async def scrape_playwright():
        results = await ascrape_playwright(url)
        #pprint.pprint(results)  # Use pprint for better readability of the list of rows
        
    asyncio.run(scrape_playwright())