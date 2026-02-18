from __future__ import annotations

from typing import Any

import httpx

from app.models import SimilarReference


LICHESS_EXPLORER_URL = "https://explorer.lichess.ovh/lichess"


async def fetch_similar_positions(fen: str, top_games: int = 3) -> list[SimilarReference]:
    params = {"fen": fen, "moves": top_games, "topGames": top_games}

    async with httpx.AsyncClient(timeout=7.0) as client:
        try:
            response = await client.get(LICHESS_EXPLORER_URL, params=params)
            response.raise_for_status()
        except Exception:
            return []

    payload: dict[str, Any] = response.json()
    references: list[SimilarReference] = []

    opening = payload.get("opening")
    if opening:
        references.append(
            SimilarReference(
                source="Lichess Opening Explorer",
                title=opening.get("name", "Opening reference"),
                url="https://lichess.org/analysis",
                summary=f"ECO: {opening.get('eco', 'N/A')} — position appears in opening databases.",
            )
        )

    for game in payload.get("topGames", [])[:top_games]:
        white = game.get("white", {}).get("name", "White")
        black = game.get("black", {}).get("name", "Black")
        gid = game.get("id", "")
        if not gid:
            continue
        references.append(
            SimilarReference(
                source="Lichess Masters",
                title=f"{white} vs {black}",
                url=f"https://lichess.org/{gid}",
                summary="Comparable high-level game reached this position or structure.",
            )
        )

    return references
