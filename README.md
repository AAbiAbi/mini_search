# Mini Search Engine (Keyword + Agentic Search)

A lightweight search engine built from scratch — featuring

- keyword-based search with ranking by click popularity, and

- agentic search powered by Google Gemini (no vector embeddings).

# 🚀 Demo Preview
[▶️ Watch Demo on GitHub](https://github.com/AAbiAbi/mini_search/releases/tag/demo)


## Features

- 🔍 Simple keyword search (SQLite-based index)

- 📄 OCR text extraction for PDFs and images (via pdfplumber + pytesseract)

- 🖥️ Minimal Flask web UI

- ⭐️ Ranking by popularity (click count)

- 🤖 “Agentic Search” mode using Gemini API to automatically expand queries

- 🧱 No Elasticsearch / Lucene — built entirely from scratch

## installation

1. Clone & Enter Project
```bash
git clone https://github.com/AAbiAbi/mini_search
cd mini_search

```

2. Activate Virtual Environment
```
source .venv311/bin/activate
```
💡 If not created yet:

```bash
/opt/homebrew/bin/python3.11 -m venv .venv311
source .venv311/bin/activate
```

2. install deps
```bash
pip install -r requirements.txt
```

3. (optional) verify core deps installation success
```bash
python -m flask --version
python -m google.generativeai --help

```

## Environment Setup

Before using Gemini API, create a `.env` file in your project root:

```bash
touch .env

```

Add your Google API key (get it from Google AI Studio
):
```bash
GEMINI_API_KEY=AIzaSy...your_key_here...

```

## Project Structure

```
mini_search/
│
├── app.py                 # Flask app (routes + search UI)
├── indexer.py             # Indexing PDFs, images, text files into SQLite
├── search_db.py           # Keyword-based search logic
├── agent_search.py        # Agentic (AI) search logic using Gemini
├── templates/
│   └── index.html         # Frontend page
├── static/
│   ├── style.css          # Simple UI styling
│   └── Input_Filings/     # (optional) Example dataset folder
├── index.db               # SQLite database after indexing
├── requirements.txt
└── README.md

```

## Usage

### Step 1: Index Documents
```
python indexer.py Input_Filings
```

This will:

- Parse all PDFs, images, and text files in the folder

- Store extracted text in index.db

- Record folder metadata (for path display)

### Step 2: Start the Search UI

```
python app.py

```

Visit http://127.0.0.1:5000

You’ll see:

- A search bar

- Two buttons: Normal Search and AI Search

- Click a result to open the original document (click count tracked)

### Step 3: Agentic (AI) Search

Click “AI Search”, enter a natural question such as:

“California insurance nonrenewal rules”

The backend will:

- Send your question to Gemini

- Generate multiple keyword-style queries

- Perform searches for each

- Merge, rank, and return 1–3 high-confidence results


## Tech Stack

Component	Library
Backend	Flask
Database	SQLite
OCR	pdfplumber, pytesseract
AI Agent	Google Gemini (google-generativeai)
Frontend	HTML + CSS

## Design Decisions

Indexing: Raw text extracted and stored in SQLite for simplicity.

Ranking: Weighted sum of keyword frequency + click popularity.

Agentic Search: Gemini used as “power user” that issues multiple keyword queries.

Fallback: If Gemini unavailable, falls back to local synonym expansion.

## Future Improvements

Add semantic ranking via embeddings (e.g., Gemini Embeddings or OpenAI Embeddings)

Add PDF viewer preview in results

Add background indexing and progress bar

Improve agent query reasoning chain
