import { useState } from "react";

interface PGNUploadProps {
  onAnalyze: (file: File) => Promise<void>;
}

export function PGNUpload({ onAnalyze }: PGNUploadProps) {
  const [file, setFile] = useState<File | null>(null);

  return (
    <section className="card">
      <h2>Upload PGN</h2>
      <input
        type="file"
        accept=".pgn"
        onChange={(event) => setFile(event.target.files?.[0] ?? null)}
      />
      <button
        onClick={async () => {
          if (file) {
            await onAnalyze(file);
          }
        }}
        disabled={!file}
      >
        Analyze Game
      </button>
    </section>
  );
}
