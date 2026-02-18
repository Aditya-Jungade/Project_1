from __future__ import annotations

import chess

from app.models import MoveCategory


def categorize_move(eval_loss_cp: int, is_best: bool) -> MoveCategory:
    if is_best:
        return "Best Move"
    if eval_loss_cp <= 20:
        return "Excellent"
    if eval_loss_cp <= 50:
        return "Good"
    if eval_loss_cp <= 120:
        return "Inaccuracy"
    if eval_loss_cp <= 250:
        return "Mistake"
    return "Blunder"


def explain_move(
    board_before: chess.Board,
    san: str,
    category: MoveCategory,
    eval_before: int,
    eval_after: int,
    best_line: list[str],
    phase: str,
) -> str:
    swing = eval_after - eval_before
    side = "White" if board_before.turn == chess.WHITE else "Black"

    if category in ("Best Move", "Excellent"):
        base = f"{side}'s move {san} was strong in the {phase}, keeping key squares and tactical ideas under control."
    elif category in ("Inaccuracy", "Mistake"):
        base = (
            f"{side}'s move {san} was a {category.lower()}, and the evaluation shifted by {abs(swing)} centipawns. "
            "This likely weakened coordination or allowed a tactical resource."
        )
    else:
        base = (
            f"{side}'s move {san} was a blunder: the position changed drastically ({abs(swing)} centipawns). "
            "Critical threats were missed, leading to a losing tactical or strategic sequence."
        )

    if best_line:
        return f"{base} Engine continuation: {' '.join(best_line)}."
    return base
