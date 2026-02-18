import { useState } from "react";

import { analyzePGN } from "./api/analyze";
import { AnalysisView } from "./components/AnalysisView";
import { PGNUpload } from "./components/PGNUpload";
import type { GameAnalysis } from "./types/analysis";

export default function App() {
  const [analysis, setAnalysis] = useState<GameAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (file: File) => {
    setLoading(true);
    setError(null);
    try {
      const result = await analyzePGN(file);
      setAnalysis(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unexpected error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <h1>Automated Chess Game Analyzer</h1>
      <PGNUpload onAnalyze={handleAnalyze} />
      {loading && <p>Analyzing game with Stockfish...</p>}
      {error && <p className="error">{error}</p>}
      {analysis && <AnalysisView analysis={analysis} />}
    </main>
  );
}
