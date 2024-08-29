from langchain.chains import create_extraction_chain, create_extraction_chain_pydantic

def extract(content:str, **kwargs):
    if 'schema_pydantic' in kwargs:
        response = create_extraction_chain_pydantic(
            pydantic_schema= kwargs["schema_pydantic"], llm= kwargs["llm"]
        ).run(content)

        response_as_dict = [item.dict() for item in response]
        return response_as_dict
        
    return create_extraction_chain(schema=schema, llm=kwargs["llm"]).run(content)