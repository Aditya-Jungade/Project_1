# Automated Chess Game Analyzer

This project provides a production-ready starter architecture for an **intelligent chess game analyzer** with:

- React + TypeScript frontend for PGN upload and annotated game display.
- FastAPI backend for PGN parsing, Stockfish analysis, phase segmentation, and natural-language annotations.
- Position matching against Lichess Opening Explorer for related games/opening references.

## Project structure

```text
Project_1/
├── backend/
│   ├── app/
│   │   ├── main.py                        # FastAPI entrypoint
│   │   ├── models.py                      # API response schemas
│   │   └── services/
│   │       ├── pgn_parser.py              # PGN ingestion + metadata extraction
│   │       ├── stockfish_engine.py        # UCI engine integration
│   │       ├── phase_segmentation.py      # Opening/Middlegame/Endgame heuristics
│   │       ├── annotation.py              # Move classification + NLG comments
│   │       ├── position_search.py         # External FEN matching (Lichess API)
│   │       └── analysis_pipeline.py       # End-to-end analysis orchestration
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── api/analyze.ts                 # HTTP client for backend /api/analyze
│   │   ├── components/PGNUpload.tsx       # PGN file upload UI
│   │   ├── components/AnalysisView.tsx    # Annotated move timeline UI
│   │   ├── types/analysis.ts              # Shared analysis types
│   │   ├── App.tsx                        # App workflow
│   │   ├── main.tsx
│   │   └── styles.css
│   ├── package.json
│   └── vite.config.ts
```

## Core functionality mapping

### 1) PGN Input & Parsing
- Frontend `PGNUpload` component accepts `.pgn` files.
- Backend `/api/analyze` endpoint validates extension and parses PGN with `python-chess`.
- Metadata (players, event, ECO/opening, result) is extracted from PGN headers.

### 2) Stockfish Engine Integration
- `StockfishAnalyzer` launches Stockfish via UCI (`python-chess.engine.SimpleEngine`).
- Every ply is evaluated before/after move.
- Best line (PV SAN sequence) is captured for explanation and move comparison.

### 3) Phase Segmentation
- `determine_phase` uses:
  - minor piece development count,
  - non-pawn/non-king material,
  - early ply threshold.
- Outputs one of `opening | middlegame | endgame` per move.

### 4) Automated Annotation & Natural Language Generation
- Centipawn loss vs engine recommendation is converted into labels:
  - `Best Move`, `Excellent`, `Good`, `Inaccuracy`, `Mistake`, `Blunder`.
- Explanations are generated in plain English including tactical/strategic impact and engine continuation.

### 5) Position Matching & Web Search
- For critical moves (`Mistake`/`Blunder`), backend queries Lichess Explorer with pre-move FEN.
- Returns opening references and similar high-level games.

## API contract

### `POST /api/analyze`
- multipart/form-data with field `file` (PGN file).
- response includes:
  - metadata,
  - per-ply move annotations,
  - summary metrics (accuracy %, critical positions).

## Run locally

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export STOCKFISH_PATH=/usr/local/bin/stockfish   # adapt as needed
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Set optional frontend env:

```bash
VITE_API_BASE=http://localhost:8000
```

## Notes

- If Stockfish is not on PATH, set `STOCKFISH_PATH` explicitly.
- The phase segmentation and annotation thresholds are intentionally heuristic and can be tuned.
- You can enrich `position_search.py` with more providers (Chess.com, custom web search APIs, opening books).
