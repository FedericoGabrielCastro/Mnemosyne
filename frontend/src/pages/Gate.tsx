import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import { Shell } from "../components/Shell";

export function Gate() {
  const [pulse, setPulse] = useState("listening for the palace…");

  useEffect(() => {
    api
      .health()
      .then((health) => setPulse(`the palace is ${health.status} · ${health.embedder}`))
      .catch(() => setPulse("the palace sleeps — wake Django on :8000"));
  }, []);

  return (
    <Shell>
      <main className="relative flex min-h-[calc(100svh-88px)] flex-col items-center justify-center px-6 py-16 text-center">
        <div className="pointer-events-none absolute inset-0 grid place-items-center opacity-70">
          <div className="relative grid place-items-center">
            <div className="ring h-[22rem] w-[22rem] rounded-full sm:h-[32rem] sm:w-[32rem]" />
            <div className="ring ring-delay absolute h-[16rem] w-[16rem] rounded-full sm:h-[24rem] sm:w-[24rem]" />
          </div>
        </div>
        <p className="relative font-sans text-[11px] tracking-[0.55em] text-gold uppercase">Titaness of Memory</p>
        <h1 className="gold-text relative mt-4 font-display text-5xl leading-none sm:text-7xl md:text-8xl">
          MNEMOSYNE
        </h1>
        <p className="relative mt-6 max-w-xl font-serif text-2xl italic text-ivory/80">
          Drink from the spring before you speak. Local RAG. Semantic search. Nothing leaves the palace unless you ask Ollama.
        </p>
        <div className="relative mt-10 flex flex-wrap items-center justify-center gap-4">
          <Link
            to="/vaults"
            className="shimmer rounded-sm border border-gold/50 bg-gold/10 px-8 py-3 font-sans text-xs tracking-[0.35em] text-gold-bright uppercase"
          >
            Enter the vaults
          </Link>
          <a
            href="#rite"
            className="rounded-sm border border-ivory/20 px-8 py-3 font-sans text-xs tracking-[0.35em] text-ivory/70 uppercase hover:border-gold/40 hover:text-gold"
          >
            The rite
          </a>
        </div>
        <p className="relative mt-8 font-sans text-[11px] tracking-[0.28em] text-ivory/45 uppercase">{pulse}</p>
        <section id="rite" className="relative mt-24 grid max-w-5xl gap-6 md:grid-cols-3">
          {[
            ["Inscribe", "Lay markdown, text, or PDF upon a vault. The palace shards it into overlapping loci."],
            ["Remember", "A local ONNX model paints each shard as a vector. The index never leaves the disk."],
            ["Ask", "Questions are embedded the same way. The oracle answers only from the nearest memories."],
          ].map(([title, copy]) => (
            <article key={title} className="marble filigree p-6 text-left">
              <h2 className="font-display text-sm tracking-[0.3em] text-gold uppercase">{title}</h2>
              <p className="mt-3 font-serif text-xl leading-relaxed text-ivory/80">{copy}</p>
            </article>
          ))}
        </section>
      </main>
    </Shell>
  );
}
