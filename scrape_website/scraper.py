# LLM Based matcher implemented by langchain
import os
from dotenv import load_dotenv

import json


def scrape_prof_websites():

    try:
        # Load environment variables from the .env file
        load_dotenv()

        # Retrieve environment variables
        data_path = os.getenv('DATA_PATH')

        with open(data_path, 'r', encoding='utf-8') as f:
            print("Loading Data ...")
            data = json.load(f)
        
        print("JSON data loaded successfully.")
                # Print the loaded data or process it as needed
        #print(data)
        
        


    except Exception as e:
            results = f"Error: {e}"

    return 0

if __name__ == "__main__":
    scrape_prof_websites()
