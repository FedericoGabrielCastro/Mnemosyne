import { type FormEvent, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import { Shell } from "../components/Shell";
import type { Vault } from "../types";

export function Vaults() {
  const [vaults, setVaults] = useState<Vault[]>([]);
  const [name, setName] = useState("");
  const [epithet, setEpithet] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const load = () => {
    api
      .vaults()
      .then(setVaults)
      .catch((err: Error) => setError(err.message));
  };

  useEffect(() => {
    load();
  }, []);

  const inscribe = async (event: FormEvent) => {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      await api.createVault(name.trim(), epithet.trim());
      setName("");
      setEpithet("");
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "The stone refused the name.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <Shell>
      <main className="mx-auto max-w-6xl px-6 py-12 md:px-10">
        <div className="flex flex-col justify-between gap-8 md:flex-row md:items-end">
          <div>
            <p className="font-sans text-[11px] tracking-[0.4em] text-gold uppercase">Wing of vaults</p>
            <h1 className="gold-text mt-2 font-display text-4xl md:text-6xl">Memory chambers</h1>
            <p className="mt-3 max-w-xl font-serif text-xl italic text-ivory/75">
              Each vault is a room in the palace. Offer manuscripts, then walk the colonnade with a question.
            </p>
          </div>
          <form onSubmit={inscribe} className="marble filigree w-full max-w-md p-5">
            <p className="font-display text-[11px] tracking-[0.3em] text-gold uppercase">Inscribe a vault</p>
            <input
              value={name}
              onChange={(event) => setName(event.target.value)}
              required
              placeholder="Name of the chamber"
              className="mt-4 w-full border-b border-gold/30 bg-transparent py-2 font-serif text-xl text-ivory outline-none placeholder:text-ivory/30"
            />
            <input
              value={epithet}
              onChange={(event) => setEpithet(event.target.value)}
              placeholder="Epithet, if it has one"
              className="mt-3 w-full border-b border-gold/20 bg-transparent py-2 font-serif text-lg italic text-ivory/80 outline-none placeholder:text-ivory/30"
            />
            <button
              disabled={busy}
              className="mt-5 w-full border border-gold/50 py-2 font-sans text-[11px] tracking-[0.3em] text-gold-bright uppercase disabled:opacity-50"
            >
              {busy ? "Carving…" : "Carve the lintel"}
            </button>
          </form>
        </div>
        {error && <p className="mt-6 font-serif text-lg text-gold">{error}</p>}
        <section className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {vaults.map((vault, index) => (
            <Link
              key={vault.id}
              to={`/vaults/${vault.id}`}
              className="marble filigree rise p-6 hover:border-gold/50"
              style={{ animationDelay: `${index * 70}ms` }}
            >
              <p className="font-sans text-[10px] tracking-[0.35em] text-gold/80 uppercase">Vault</p>
              <h2 className="mt-2 font-display text-2xl text-gold-bright">{vault.name}</h2>
              <p className="mt-2 min-h-12 font-serif text-lg italic text-ivory/70">{vault.epithet || "An unnamed wing."}</p>
              <p className="mt-6 font-sans text-[11px] tracking-[0.25em] text-ivory/50 uppercase">
                {vault.document_count} offering{vault.document_count === 1 ? "" : "s"}
              </p>
            </Link>
          ))}
          {!vaults.length && !error && (
            <p className="font-serif text-2xl italic text-ivory/50">The colonnade is empty. Inscribe the first vault.</p>
          )}
        </section>
      </main>
    </Shell>
  );
}
