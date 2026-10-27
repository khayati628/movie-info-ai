import json
import os
import sys

import pytest
from langchain_core.language_models.fake_chat_models import FakeListChatModel

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extractor import MovieInfo, build_chain, extract_movie_info

FAKE_RESPONSE = json.dumps(
    {
        "title": "Inception",
        "release_year": 2010,
        "genre": ["Sci-Fi", "Thriller"],
        "director": "Christopher Nolan",
        "cast": ["Leonardo DiCaprio", "Elliot Page"],
        "rating": 8.8,
        "synopsis": "A thief enters people's dreams to steal secrets.",
    }
)


def test_extracts_structured_info():
    chain = build_chain(FakeListChatModel(responses=[FAKE_RESPONSE]))
    info = extract_movie_info("Inception is a 2010 film...", chain=chain)
    assert isinstance(info, MovieInfo)
    assert info.title == "Inception"
    assert info.release_year == 2010
    assert info.director == "Christopher Nolan"


def test_optional_fields_default_when_missing():
    minimal = json.dumps({"title": "Untitled", "synopsis": "A short film."})
    chain = build_chain(FakeListChatModel(responses=[minimal]))
    info = extract_movie_info("Some text", chain=chain)
    assert info.release_year is None
    assert info.genre == []
    assert info.cast == []


def test_handles_json_in_markdown_fence():
    fenced = f"```json\n{FAKE_RESPONSE}\n```"
    chain = build_chain(FakeListChatModel(responses=[fenced]))
    assert extract_movie_info("text", chain=chain).title == "Inception"


def test_empty_input_rejected():
    with pytest.raises(ValueError):
        extract_movie_info("   ")


def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("MISTRAL_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        build_chain()
