import os
from typing import List, Optional

from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from pydantic import BaseModel, Field

load_dotenv()

DEFAULT_MODEL = "open-mistral-7b"


class MovieInfo(BaseModel):
    title: str = Field(description="The title of the movie")
    release_year: Optional[int] = Field(
        default=None, description="The year the movie was released"
    )
    genre: List[str] = Field(
        default_factory=list, description="The genres of the movie"
    )
    director: Optional[str] = Field(
        default=None, description="The director of the movie"
    )
    cast: List[str] = Field(
        default_factory=list, description="The main cast members"
    )
    rating: Optional[float] = Field(
        default=None, description="The rating of the movie"
    )
    synopsis: str = Field(description="A short summary of the movie plot")


parser = PydanticOutputParser(pydantic_object=MovieInfo)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Extract movie information from the paragraph. "
            "Only use facts stated in the text; leave a field empty if it is not mentioned.\n\n"
            "{format_instructions}",
        ),
        ("human", "Analyze this paragraph:\n{text}"),
    ]
).partial(format_instructions=parser.get_format_instructions())


def build_chain(model=None):
    if model is None:
        if not os.getenv("MISTRAL_API_KEY"):
            raise RuntimeError(
                "MISTRAL_API_KEY is not set. Copy .env.example to .env and add your key."
            )
        model = ChatMistralAI(
            model=os.getenv("MISTRAL_MODEL", DEFAULT_MODEL), temperature=0
        )
    return prompt | model | parser


def extract_movie_info(text: str, chain=None) -> MovieInfo:
    if not text or not text.strip():
        raise ValueError("Please provide a movie paragraph.")
    chain = chain or build_chain()
    return chain.invoke({"text": text})
