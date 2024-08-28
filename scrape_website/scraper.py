# LLM Based matcher implemented by langchain
import os
from dotenv import load_dotenv

import json

from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer


def scrape_prof_websites():

    try:
        # Load environment variables from the .env file
        load_dotenv()

        # Retrieve environment variables
        data_path = os.getenv('DATA_PATH')
        user_agent = os.getenv('USER_AGENT')

        with open(data_path, 'r', encoding='utf-8') as f:
            print("Loading Data ...")
            data = json.load(f)
        
        print("JSON data loaded successfully.")
                # Print the loaded data or process it as needed
        #print(data)
        

        for k,v in data.items():
            university_name = k

            for prof in v:
                name = prof['name']
                research_area = prof['area']
                url = prof['url']

                print(url)
            
                loader = AsyncChromiumLoader([url], user_agent=user_agent)
                html = loader.load()

                bs_transformer = BeautifulSoupTransformer()
                docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["li", "a", "span", "div", "h1", "h2", "h3"])

                extracted_data = docs_transformed[0].page_content[0:16000]

                print(extracted_data)

                break

            break






    except Exception as e:
            results = f"Error: {e}"

    return 0

if __name__ == "__main__":
    scrape_prof_websites()
