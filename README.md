# Merch Trend Intelligence Engine

A private, local-only web application for Amazon Merch on Demand sellers to identify early-stage trending phrases, reusable patterns, and original phrase twists.

## Features

- **Trend Detection**: Early-stage trending phrase identification
- **Pattern Recognition**: Reusable phrase patterns and frameworks
- **Trademark Safety**: USPTO trademark checking and risk scoring
- **SEO Generation**: Merch-compliant listing content generation
- **Multi-Source Scraping**: Reddit, Google Trends, Amazon, Etsy, and more

## Tech Stack

### Backend
- Python 3.11 with FastAPI
- SQLite with SQLAlchemy
- spaCy, scikit-learn, sentence-transformers for NLP

### Frontend
- React with Vite
- Tailwind CSS
- Recharts for visualization

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
merch_trend_engine/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── routes/
│   │   └── services/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   └── package.json
└── data/
    ├── raw/
    ├── processed/
    └── trademarks/
```

## License

Private use only. Not for distribution.
