export type Phase = "opening" | "middlegame" | "endgame";

export interface SimilarReference {
  source: string;
  title: string;
  url: string;
  summary: string;
}

export interface AnnotatedMove {
  ply: number;
  turn: number;
  side: "white" | "black";
  san: string;
  uci: string;
  fen_before: string;
  fen_after: string;
  phase: Phase;
  eval_before_cp: number;
  eval_after_cp: number;
  best_eval_cp: number;
  eval_loss_cp: number;
  category: string;
  explanation: string;
  best_line: string[];
  references: SimilarReference[];
}

export interface GameAnalysis {
  metadata: {
    event?: string;
    site?: string;
    date?: string;
    round?: string;
    white?: string;
    black?: string;
    result?: string;
    eco?: string;
    opening?: string;
  };
  total_plies: number;
  moves: AnnotatedMove[];
  summary: {
    white_accuracy: number;
    black_accuracy: number;
    critical_positions: number;
  };
}
