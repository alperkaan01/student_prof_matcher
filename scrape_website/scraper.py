import os
from dotenv import load_dotenv

import json
from tqdm import tqdm

from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.llms import huggingface_hub

from schema.schema import ProfProfile
from extract import extract



def scrape_prof_websites():
    try:
        # Load environment variables from the .env file
        load_dotenv()

        # Retrieve environment variables
        data_path = os.getenv('DATA_PATH')
        user_agent = os.getenv('USER_AGENT')
        openai_api_key = os.getenv('OPENAI_API_KEY')

        with open(data_path, 'r', encoding='utf-8') as f:
            print("Loading Data ...")
            data = json.load(f)
        
        print("JSON data loaded successfully.")

        # Define the llm
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125", openai_api_key=openai_api_key)

        # llm = huggingface_hub(repo_id="meta-llama/Meta-Llama-3.1-70B-Instruct")



        for k, v in data.items():
            university_name = k
            print(f"Extraction is started for {university_name}")

            # Add tqdm for progress tracking
            for prof in tqdm(v, desc=f"Processing professors for {university_name}"):
                name = prof['name']
                research_area = prof['area']
                url = prof['url']

                loader = AsyncChromiumLoader([url], user_agent=user_agent)
                html = loader.load()

                bs_transformer = BeautifulSoupTransformer()
                docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["li", "a", "span", "div", "h1", "h2", "h3"])

                # print(f"Data is extracted for the professor {name}")
                extracted_data = docs_transformed[0].page_content[0:4000]

                extracted_content = extract(content=extracted_data, schema_pydantic=ProfProfile, llm= llm)
                pprint.pprint(extracted_content)

                break  # This is just for testing; remove this in production.

            break  # This is just for testing; remove this in production.

    except Exception as e:
        results = f"Error: {e}"
        print(results)

    return 0

if __name__ == "__main__":

    scrape_prof_websites()
