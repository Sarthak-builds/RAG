# Ingestion & Retrieval Architecture (Short)

## Pipeline overview

```
DATA/ (PDF, DOCX, PPTX, HTML, TXT)
  -> app/loaders/*        (extract plain text per format)
  -> app/ingestion/processor.py   (route file -> correct loader)
  -> app/ingestion/chunking       (split long text into ~500-token chunks)
  -> app/services/retrieval/embeddings.py (chunk -> vector)
  -> Qdrant                       (store + semantic search)
```

## Why this exists

Qdrant only stores vectors, so every document must become plain text,
then chunks, then embeddings. Mixed formats need a parser each:

| File | Handles | Library |
|------|---------|---------|
| `app/loaders/pdf.py` | PDFs | pypdf, fallback pdfplumber for image-heavy pages |
| `app/loaders/office.py` | DOCX / PPTX | unstructured (keeps headings / slide structure) |
| `app/loaders/html.py` | HTML | BeautifulSoup (strips script/style/meta) |
| `app/loaders/text.py` | TXT | plain UTF-8 read |

All loaders emit logfire spans so failures are traceable in production.

## Module roles

- `app/config.py` — single `Settings` class; all env vars (Groq, fallback key, Gemini, Qdrant key + endpoint) loaded via `python-dotenv`
- `app/ingestion/processor.py` — routes each file by extension to its loader
- `app/ingestion/chunking/splitter.py` — chunk text for embedding (embeddings capture short-passage meaning)
- `app/services/retrieval/embeddings.py` — embed chunks (Gemini)
- `app/services/retrieval/` — Qdrant storage, ranking / reranking
- LLM: Groq `llama-3.3-70b-versatile` (free tier, rate-limited; fallback key on cap)
