from __future__ import annotations

import io
from dataclasses import dataclass

import chess.pgn

from app.models import GameMetadata


@dataclass
class ParsedGame:
    metadata: GameMetadata
    game: chess.pgn.Game


def parse_pgn(pgn_text: str) -> ParsedGame:
    pgn_io = io.StringIO(pgn_text)
    game = chess.pgn.read_game(pgn_io)
    if game is None:
        raise ValueError("Could not parse PGN. Ensure the file contains a valid game.")

    headers = game.headers
    metadata = GameMetadata(
        event=headers.get("Event"),
        site=headers.get("Site"),
        date=headers.get("Date"),
        round=headers.get("Round"),
        white=headers.get("White"),
        black=headers.get("Black"),
        result=headers.get("Result"),
        eco=headers.get("ECO"),
        opening=headers.get("Opening"),
    )
    return ParsedGame(metadata=metadata, game=game)
