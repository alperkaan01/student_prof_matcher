#create a schema for langchain extraction chain
from typing import Optional

from langchain_core.pydantic_v1 import BaseModel, Field

class ProfProfile(BaseModel):
    """Information about a person."""

    # ^ Doc-string for the entity Person.
    # This doc-string is sent to the LLM as the description of the schema Person,
    # and it can help to improve extraction results.

    # Note that:
    # 1. Each field is an `optional` -- this allows the model to decline to extract it!
    # 2. Each field has a `description` -- this description is used by the LLM.
    # Having a good description can help improve extraction results.
    about_me: Optional[str] = Field(default=None, description="Description of the Professor which summarizes his or her interests. It could be located under the about me section or it could directly emerge as a paragraph on the top of the page.")

    research_interests: Optional[str] = Field(
        default=None, description="The topic list of the research interests of the professor if known."
    )
    
    research_list: Optional[str] = Field(
        default=None, description="Titles of the research professor have conducted. Brief description of each research if known."
    )

    previous_students: Optional[str] = Field(
        default=None, description= "Previous student alumnis and their positions if known"
    )