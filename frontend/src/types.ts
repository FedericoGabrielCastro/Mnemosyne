export type Vault = {
  id: string;
  name: string;
  slug: string;
  epithet: string;
  document_count: number;
  created_at: string;
};

export type MemoryDocument = {
  id: string;
  title: string;
  original_filename: string;
  mime_type: string;
  status: "pending" | "indexed" | "failed";
  chunk_count: number;
  character_count: number;
  error_message: string;
  created_at: string;
  indexed_at: string | null;
};

export type SearchHit = {
  document_id: string;
  chunk_id: string;
  title: string;
  text: string;
  score: number;
};

export type AskResult = {
  question: string;
  answer: string;
  mode: "extractive" | "generative";
  citations: SearchHit[];
};
