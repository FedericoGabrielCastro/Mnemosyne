import type { AskResult, MemoryDocument, SearchHit, Vault } from "./types";

const API = import.meta.env.VITE_API_URL ?? "";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API}${path}`, init);
  if (response.status === 204) {
    return undefined as T;
  }
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(formatError(payload) || response.statusText);
  }
  return payload as T;
}

function formatError(payload: unknown): string {
  if (!payload || typeof payload !== "object") {
    return "";
  }
  const body = payload as Record<string, unknown>;
  if (typeof body.detail === "string") {
    return body.detail;
  }
  const first = Object.values(body)[0];
  if (Array.isArray(first) && typeof first[0] === "string") {
    return first[0];
  }
  return "";
}

export const api = {
  health: () => request<{ name: string; status: string; embedder: string }>("/api/health/"),
  vaults: () => request<Vault[]>("/api/vaults/"),
  createVault: (name: string, epithet: string) =>
    request<Vault>("/api/vaults/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, epithet }),
    }),
  vault: (id: string) => request<Vault>(`/api/vaults/${id}/`),
  documents: (vaultId: string) => request<MemoryDocument[]>(`/api/vaults/${vaultId}/documents/`),
  offer: (vaultId: string, file: File, title?: string) => {
    const body = new FormData();
    body.append("file", file);
    if (title) {
      body.append("title", title);
    }
    return request<MemoryDocument>(`/api/vaults/${vaultId}/documents/`, { method: "POST", body });
  },
  forget: (vaultId: string, documentId: string) =>
    request<void>(`/api/vaults/${vaultId}/documents/${documentId}/`, { method: "DELETE" }),
  search: (vaultId: string, query: string, topK = 5) =>
    request<{ query: string; hits: SearchHit[] }>(`/api/vaults/${vaultId}/search/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, top_k: topK }),
    }),
  ask: (vaultId: string, question: string, topK = 5) =>
    request<AskResult>(`/api/vaults/${vaultId}/ask/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, top_k: topK }),
    }),
};
