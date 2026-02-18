from __future__ import annotations

import chess

from app.models import AnalysisSummary, AnnotatedMove, GameAnalysis
from app.services.annotation import categorize_move, explain_move
from app.services.pgn_parser import ParsedGame
from app.services.phase_segmentation import determine_phase
from app.services.position_search import fetch_similar_positions
from app.services.stockfish_engine import StockfishAnalyzer


def _side_eval_loss(white_pov_loss: int, side_to_move: chess.Color) -> int:
    return white_pov_loss if side_to_move == chess.WHITE else -white_pov_loss


def _clamp_accuracy(loss_cp: int) -> float:
    return max(0.0, min(100.0, 100 - (loss_cp / 8.0)))


async def analyze_game(parsed: ParsedGame) -> GameAnalysis:
    game = parsed.game
    node = game
    board = game.board()
    ply = 0
    annotated: list[AnnotatedMove] = []
    white_losses: list[int] = []
    black_losses: list[int] = []

    with StockfishAnalyzer() as engine:
        while node.variations:
            next_node = node.variation(0)
            move = next_node.move
            ply += 1
            turn = (ply + 1) // 2
            side_label = "white" if board.turn == chess.WHITE else "black"
            side_to_move = board.turn

            board_before = board.copy(stack=False)
            fen_before = board.fen()
            phase = determine_phase(board, ply)
            eval_before, pv_before = engine.evaluate(board)

            san = board.san(move)
            uci = move.uci()

            board.push(move)
            fen_after = board.fen()
            eval_after, _ = engine.evaluate(board)

            board.pop()
            best_move = None
            try:
                if pv_before:
                    best_move = board.parse_san(pv_before[0])
            except ValueError:
                best_move = None

            board.push(move)

            if best_move is None:
                eval_loss = abs(eval_after - eval_before)
                is_best = False
            else:
                if side_to_move == chess.WHITE:
                    eval_loss = max(0, eval_before - eval_after)
                else:
                    eval_loss = max(0, eval_after - eval_before)
                is_best = move == best_move

            category = categorize_move(eval_loss, is_best=is_best)
            explanation = explain_move(
                board_before=board_before,
                san=san,
                category=category,
                eval_before=eval_before,
                eval_after=eval_after,
                best_line=pv_before,
                phase=phase,
            )

            references = []
            if category in ("Blunder", "Mistake"):
                references = await fetch_similar_positions(fen_before)

            entry = AnnotatedMove(
                ply=ply,
                turn=turn,
                side=side_label,
                san=san,
                uci=uci,
                fen_before=fen_before,
                fen_after=fen_after,
                phase=phase,
                eval_before_cp=eval_before,
                eval_after_cp=eval_after,
                best_eval_cp=eval_before,
                eval_loss_cp=eval_loss,
                category=category,
                explanation=explanation,
                best_line=pv_before,
                references=references,
            )
            annotated.append(entry)

            if side_label == "white":
                white_losses.append(eval_loss)
            else:
                black_losses.append(eval_loss)

            node = next_node

    white_accuracy = (
        sum(_clamp_accuracy(v) for v in white_losses) / len(white_losses) if white_losses else 0.0
    )
    black_accuracy = (
        sum(_clamp_accuracy(v) for v in black_losses) / len(black_losses) if black_losses else 0.0
    )
    critical = sum(1 for m in annotated if m.category in ("Mistake", "Blunder"))

    return GameAnalysis(
        metadata=parsed.metadata,
        total_plies=ply,
        moves=annotated,
        summary=AnalysisSummary(
            white_accuracy=round(white_accuracy, 2),
            black_accuracy=round(black_accuracy, 2),
            critical_positions=critical,
        ),
    )
