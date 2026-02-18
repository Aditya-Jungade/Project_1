from __future__ import annotations

import os
from dataclasses import dataclass

import chess
import chess.engine


@dataclass
class EngineConfig:
    path: str = os.getenv("STOCKFISH_PATH", "stockfish")
    depth: int = int(os.getenv("STOCKFISH_DEPTH", "14"))
    multipv: int = int(os.getenv("STOCKFISH_MULTIPV", "2"))


class StockfishAnalyzer:
    def __init__(self, config: EngineConfig | None = None) -> None:
        self.config = config or EngineConfig()
        self._engine: chess.engine.SimpleEngine | None = None

    def __enter__(self) -> "StockfishAnalyzer":
        self._engine = chess.engine.SimpleEngine.popen_uci(self.config.path)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._engine:
            self._engine.quit()

    @property
    def engine(self) -> chess.engine.SimpleEngine:
        if not self._engine:
            raise RuntimeError("StockfishAnalyzer is not initialized. Use context manager.")
        return self._engine

    def evaluate(self, board: chess.Board) -> tuple[int, list[str]]:
        info = self.engine.analyse(
            board,
            chess.engine.Limit(depth=self.config.depth),
            multipv=self.config.multipv,
        )

        best = info[0] if isinstance(info, list) else info
        score = best["score"].pov(chess.WHITE)
        score_cp = _normalize_score(score)

        pv_moves = best.get("pv", [])
        pv_san = _pv_to_san(board, pv_moves)
        return score_cp, pv_san


def _normalize_score(score: chess.engine.PovScore) -> int:
    mate = score.mate()
    if mate is not None:
        # Positive means white mating, negative means black mating.
        return 100000 if mate > 0 else -100000
    cp = score.score()
    return cp if cp is not None else 0


def _pv_to_san(board: chess.Board, pv: list[chess.Move], max_len: int = 6) -> list[str]:
    line: list[str] = []
    temp = board.copy()
    for move in pv[:max_len]:
        line.append(temp.san(move))
        temp.push(move)
    return line
