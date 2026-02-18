from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


PhaseName = Literal["opening", "middlegame", "endgame"]
MoveCategory = Literal[
    "Brilliant",
    "Best Move",
    "Excellent",
    "Good",
    "Inaccuracy",
    "Mistake",
    "Blunder",
]


class GameMetadata(BaseModel):
    event: str | None = None
    site: str | None = None
    date: str | None = None
    round: str | None = None
    white: str | None = None
    black: str | None = None
    result: str | None = None
    eco: str | None = None
    opening: str | None = None


class EngineLine(BaseModel):
    score_cp: int
    mate: int | None = None
    pv_san: list[str] = Field(default_factory=list)


class SimilarReference(BaseModel):
    source: str
    title: str
    url: str
    summary: str


class AnnotatedMove(BaseModel):
    ply: int
    turn: int
    side: Literal["white", "black"]
    san: str
    uci: str
    fen_before: str
    fen_after: str
    phase: PhaseName
    eval_before_cp: int
    eval_after_cp: int
    best_eval_cp: int
    eval_loss_cp: int
    category: MoveCategory
    explanation: str
    best_line: list[str] = Field(default_factory=list)
    references: list[SimilarReference] = Field(default_factory=list)


class AnalysisSummary(BaseModel):
    white_accuracy: float
    black_accuracy: float
    critical_positions: int


class GameAnalysis(BaseModel):
    metadata: GameMetadata
    total_plies: int
    moves: list[AnnotatedMove]
    summary: AnalysisSummary

