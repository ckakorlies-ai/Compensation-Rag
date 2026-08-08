# KenteCode AI Assistant

A retrieval-augmented AI assistant for KenteCode documentation that uses PDF sources and returns answers with explicit citations.

## What this project includes
- Backend service built with FastAPI
- PDF ingestion and chunking with page-aware metadata
- Local vector store using OpenAI embeddings and cosine similarity
- Query endpoint that returns answers plus PDF citations

## Setup
1. Install dependencies:

```bash
pip install -r requirements.txt
```

On Windows PowerShell, run:

```powershell
python -m pip install -r requirements.txt
```

2. Set your OpenAI API key in a `.env` file at the workspace root:

```bash
copy .env.example .env
```

Then edit `.env` and replace the placeholder with your actual key:

```text
OPENAI_API_KEY=your_api_key_here
```

> Do not commit `.env` or any real API keys to source control. Use `.env.example` as a template instead.

3. Add KenteCode PDF documentation files to the `docs/` folder.

## Run the backend server

```bash
uvicorn backend.main:app --reload
```

## Run the Streamlit interface

```bash
streamlit run streamlit_app.py
```

## Run with Docker

1. Create a `.env` file containing your OpenAI key:

```text
OPENAI_API_KEY=your_api_key_here
```

2. Build and start services:

```bash
docker compose up --build
```

3. Visit `http://localhost:8501` for the Streamlit UI.

## API Endpoints
- `POST /ingest` — ingest PDFs from `docs/` and build the local index
- `POST /query` — ask a question and get an answer with citations

## Usage
1. Put PDF files in `docs/`
2. Call `POST /ingest`
3. Call `POST /query` with JSON body:

```json
{
  "question": "How do I configure KenteCode authentication?"
}
```

## Notes
- The assistant is designed to answer using only the ingested PDF documentation.
- Answers include citations in the form `source file, page number`.
