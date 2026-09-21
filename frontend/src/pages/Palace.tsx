import { type FormEvent, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api";
import { Shell } from "../components/Shell";
import { Shard } from "../components/Shard";
import type { AskResult, MemoryDocument, SearchHit, Vault } from "../types";

type Rite = "ask" | "search";

export function Palace() {
  const { vaultId = "" } = useParams();
  const [vault, setVault] = useState<Vault | null>(null);
  const [documents, setDocuments] = useState<MemoryDocument[]>([]);
  const [rite, setRite] = useState<Rite>("ask");
  const [query, setQuery] = useState("");
  const [hits, setHits] = useState<SearchHit[]>([]);
  const [oracle, setOracle] = useState<AskResult | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [drag, setDrag] = useState(false);

  const refresh = () => {
    api.vault(vaultId).then(setVault).catch((err: Error) => setError(err.message));
    api.documents(vaultId).then(setDocuments).catch((err: Error) => setError(err.message));
  };

  useEffect(() => {
    refresh();
  }, [vaultId]);

  const offer = async (files: FileList | null) => {
    if (!files?.length) {
      return;
    }
    setBusy(true);
    setError("");
    try {
      for (const file of Array.from(files)) {
        await api.offer(vaultId, file);
      }
      refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "The offering was refused.");
    } finally {
      setBusy(false);
    }
  };

  const consult = async (event: FormEvent) => {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      if (rite === "search") {
        const result = await api.search(vaultId, query);
        setHits(result.hits);
        setOracle(null);
      } else {
        const result = await api.ask(vaultId, query);
        setOracle(result);
        setHits(result.citations);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "The oracle did not answer.");
    } finally {
      setBusy(false);
    }
  };

  const forget = async (documentId: string) => {
    await api.forget(vaultId, documentId);
    refresh();
  };

  return (
    <Shell>
      <main className="mx-auto grid max-w-7xl gap-8 px-6 py-10 lg:grid-cols-[minmax(0,0.9fr)_minmax(0,1.2fr)] md:px-10">
        <section>
          <p className="font-sans text-[11px] tracking-[0.4em] text-gold uppercase">Chamber</p>
          <h1 className="gold-text mt-2 font-display text-4xl">{vault?.name ?? "…"}</h1>
          <p className="mt-2 font-serif text-xl italic text-ivory/70">{vault?.epithet}</p>

          <label
            onDragOver={(event) => {
              event.preventDefault();
              setDrag(true);
            }}
            onDragLeave={() => setDrag(false)}
            onDrop={(event) => {
              event.preventDefault();
              setDrag(false);
              void offer(event.dataTransfer.files);
            }}
            className={`marble filigree mt-8 block cursor-pointer p-8 text-center ${drag ? "border-gold" : ""}`}
          >
            <p className="font-display text-sm tracking-[0.28em] text-gold uppercase">Lay your pages upon the stone</p>
            <p className="mt-3 font-serif text-lg text-ivory/70">Markdown, text, or PDF. The palace will shard them into memory.</p>
            <input
              type="file"
              className="hidden"
              accept=".txt,.md,.markdown,.pdf"
              multiple
              onChange={(event) => {
                void offer(event.target.files);
                event.target.value = "";
              }}
            />
          </label>

          <ul className="mt-6 space-y-3">
            {documents.map((document) => (
              <li key={document.id} className="marble flex items-start justify-between gap-4 p-4">
                <div>
                  <p className="font-display text-base text-gold-bright">{document.title}</p>
                  <p className="font-sans text-[11px] tracking-[0.18em] text-ivory/50 uppercase">
                    {document.status} · {document.chunk_count} shards
                  </p>
                  {document.error_message && (
                    <p className="mt-1 font-serif text-sm text-gold">{document.error_message}</p>
                  )}
                </div>
                <button
                  onClick={() => void forget(document.id)}
                  className="font-sans text-[10px] tracking-[0.2em] text-ivory/40 uppercase hover:text-gold"
                >
                  Forget
                </button>
              </li>
            ))}
          </ul>
        </section>

        <section className="marble filigree p-6 md:p-8">
          <div className="flex gap-6">
            {(["ask", "search"] as const).map((mode) => (
              <button
                key={mode}
                onClick={() => setRite(mode)}
                className={`font-sans text-[11px] tracking-[0.32em] uppercase ${rite === mode ? "text-gold-bright" : "text-ivory/40"}`}
              >
                {mode === "ask" ? "Oracle" : "Semantic search"}
              </button>
            ))}
          </div>
          <form onSubmit={consult} className="mt-6">
            <textarea
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              required
              rows={3}
              placeholder={rite === "ask" ? "Ask what the palace remembers…" : "Search the loci by intent…"}
              className="w-full resize-none bg-transparent font-serif text-2xl italic text-ivory outline-none placeholder:text-ivory/30"
            />
            <button
              disabled={busy}
              className="mt-4 border border-gold/50 px-6 py-2 font-sans text-[11px] tracking-[0.3em] text-gold-bright uppercase disabled:opacity-50"
            >
              {busy ? "Descending…" : rite === "ask" ? "Consult" : "Search"}
            </button>
          </form>
          {error && <p className="mt-4 font-serif text-lg text-gold">{error}</p>}
          {oracle && (
            <div className="parchment rise mt-8 p-5">
              <p className="font-sans text-[10px] tracking-[0.3em] text-gold uppercase">{oracle.mode} recollection</p>
              <p className="mt-3 whitespace-pre-wrap font-serif text-xl leading-relaxed text-ivory">{oracle.answer}</p>
            </div>
          )}
          <div className="mt-6 space-y-4">
            {hits.map((hit, index) => (
              <Shard key={hit.chunk_id} hit={hit} index={index} />
            ))}
          </div>
        </section>
      </main>
    </Shell>
  );
}
