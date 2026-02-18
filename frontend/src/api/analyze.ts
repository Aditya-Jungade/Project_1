import type { GameAnalysis } from "../types/analysis";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

export async function analyzePGN(file: File): Promise<GameAnalysis> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/api/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(payload.detail ?? "Failed to analyze PGN");
  }

  return (await response.json()) as GameAnalysis;
}
