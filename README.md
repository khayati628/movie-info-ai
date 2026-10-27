# 🎬 Movie Information AI

Paste any movie text (a review, a plot summary, a Wikipedia blurb) and get clean, structured data back. Built with LangChain, Mistral AI and Pydantic, with both a Streamlit web UI and a terminal CLI.

## Example

**Input**

> Inception is a 2010 sci-fi thriller directed by Christopher Nolan, starring Leonardo DiCaprio and Elliot Page. A thief who steals secrets through dream-sharing is offered a chance to erase his criminal record by planting an idea in a target's mind. Rated 8.8 on IMDb.

**Output**

```json
{
  "title": "Inception",
  "release_year": 2010,
  "genre": ["Sci-Fi", "Thriller"],
  "director": "Christopher Nolan",
  "cast": ["Leonardo DiCaprio", "Elliot Page"],
  "rating": 8.8,
  "synopsis": "A thief who steals secrets through dream-sharing is offered a chance to erase his criminal record by planting an idea in a target's mind."
}
```

## Features

- Extracts title, release year, genres, director, cast, rating and synopsis
- Output is validated against a Pydantic schema, so fields always have the right types
- Missing details come back empty instead of being invented
- Two interfaces: Streamlit web app and CLI (reads from a prompt or a text file)
- Model is configurable through an environment variable

## Tech Stack

Python 3.10+, [LangChain](https://www.langchain.com/), [Mistral AI](https://mistral.ai/), [Pydantic](https://docs.pydantic.dev/), [Streamlit](https://streamlit.io/)

## Project Structure

```
movie-info-ai/
├── extractor.py        # Schema, prompt and LangChain pipeline (shared logic)
├── app.py              # Streamlit web interface
├── cli.py              # Command-line interface
├── tests/
│   └── test_extractor.py
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/khayati628/movie-info-ai
   cd movie-info-ai
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API key**

   Get a key from the [Mistral AI Console](https://console.mistral.ai/api-keys/), then:
   ```bash
   cp .env.example .env
   ```
   and edit `.env`:
   ```env
   MISTRAL_API_KEY="your_mistral_api_key_here"
   ```

## Usage

### Web app

```bash
streamlit run app.py
```

Paste a paragraph into the text box and click **Extract Information**.

### Command line

```bash
python cli.py                      # prompts for a paragraph
python cli.py --file movie.txt     # reads the paragraph from a file
```

The result is printed as JSON.

## Configuration

| Variable          | Required | Default            | Description                    |
| ----------------- | -------- | ------------------ | ------------------------------ |
| `MISTRAL_API_KEY` | Yes      | none               | Your Mistral AI API key        |
| `MISTRAL_MODEL`   | No       | `open-mistral-7b`  | Mistral model used for extraction |

## Running Tests

The tests use a fake model, so no API key or network access is needed.

```bash
pip install pytest
pytest
```

## How It Works

1. The text is wrapped in a prompt that includes format instructions generated from the `MovieInfo` Pydantic schema.
2. Mistral returns JSON matching that schema.
3. `PydanticOutputParser` validates the response and returns a typed `MovieInfo` object.

The whole pipeline is a single LangChain chain: `prompt | model | parser`.

## Limitations

- Accuracy depends on the model; the default `open-mistral-7b` is small and can occasionally miss fields or return malformed JSON. Try a larger model via `MISTRAL_MODEL` if that happens.
- Only information present in the pasted text is extracted. The app does not look anything up online.

## License

MIT, see [LICENSE](LICENSE).
