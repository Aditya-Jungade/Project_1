from __future__ import annotations

import chess

from app.models import PhaseName


def _non_pawn_non_king_material(board: chess.Board) -> int:
    values = {
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
    }
    total = 0
    for piece_type, value in values.items():
        total += len(board.pieces(piece_type, chess.WHITE)) * value
        total += len(board.pieces(piece_type, chess.BLACK)) * value
    return total


def _minor_development_count(board: chess.Board) -> int:
    developed = 0
    white_home = {chess.B1, chess.G1, chess.C1, chess.F1}
    black_home = {chess.B8, chess.G8, chess.C8, chess.F8}

    for square in white_home:
        piece = board.piece_at(square)
        if piece is None or piece.color != chess.WHITE or piece.piece_type not in (chess.KNIGHT, chess.BISHOP):
            developed += 1

    for square in black_home:
        piece = board.piece_at(square)
        if piece is None or piece.color != chess.BLACK or piece.piece_type not in (chess.KNIGHT, chess.BISHOP):
            developed += 1

    return developed


def determine_phase(board: chess.Board, ply: int) -> PhaseName:
    developed_pieces = _minor_development_count(board)
    material = _non_pawn_non_king_material(board)

    if material <= 20:
        return "endgame"
    if ply <= 20 and developed_pieces < 6:
        return "opening"
    return "middlegame"
