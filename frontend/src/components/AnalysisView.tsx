import type { GameAnalysis } from "../types/analysis";

interface AnalysisViewProps {
  analysis: GameAnalysis;
}

function colorForCategory(category: string) {
  if (category === "Blunder") return "#b91c1c";
  if (category === "Mistake") return "#ea580c";
  if (category === "Inaccuracy") return "#ca8a04";
  if (category === "Best Move") return "#15803d";
  return "#334155";
}

export function AnalysisView({ analysis }: AnalysisViewProps) {
  return (
    <section className="card">
      <h2>Annotated Analysis</h2>
      <p>
        <strong>{analysis.metadata.white}</strong> vs <strong>{analysis.metadata.black}</strong> ({analysis.metadata.result})
      </p>
      <p>
        Opening: {analysis.metadata.opening ?? "Unknown"} {analysis.metadata.eco ? `(${analysis.metadata.eco})` : ""}
      </p>

      <div className="summary-grid">
        <div>White accuracy: {analysis.summary.white_accuracy}%</div>
        <div>Black accuracy: {analysis.summary.black_accuracy}%</div>
        <div>Critical positions: {analysis.summary.critical_positions}</div>
      </div>

      <ul className="move-list">
        {analysis.moves.map((move) => (
          <li key={move.ply} className="move-item">
            <div className="move-header">
              <span>
                {move.turn}. {move.side === "white" ? move.san : `... ${move.san}`}
              </span>
              <span style={{ color: colorForCategory(move.category), fontWeight: 700 }}>{move.category}</span>
            </div>
            <p>{move.explanation}</p>
            <small>
              Phase: {move.phase} | Eval Loss: {move.eval_loss_cp} cp | FEN: {move.fen_before}
            </small>
            {move.best_line.length > 0 && <p>Engine line: {move.best_line.join(" ")}</p>}
            {move.references.length > 0 && (
              <ul>
                {move.references.map((ref) => (
                  <li key={ref.url}>
                    <a href={ref.url} target="_blank" rel="noreferrer">
                      {ref.source}: {ref.title}
                    </a>
                    <span> — {ref.summary}</span>
                  </li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
}
