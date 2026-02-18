from __future__ import annotations

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.models import GameAnalysis
from app.services.analysis_pipeline import analyze_game
from app.services.pgn_parser import parse_pgn

app = FastAPI(title="Chess Analyzer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analyze", response_model=GameAnalysis)
async def analyze_pgn(file: UploadFile = File(...)) -> GameAnalysis:
    if not file.filename.lower().endswith(".pgn"):
        raise HTTPException(status_code=400, detail="Please upload a .pgn file")

    raw = await file.read()
    try:
        pgn_text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="PGN must be UTF-8 encoded") from exc

    try:
        parsed = parse_pgn(pgn_text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        return await analyze_game(parsed)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=500,
            detail="Stockfish executable not found. Set STOCKFISH_PATH environment variable.",
        ) from exc
