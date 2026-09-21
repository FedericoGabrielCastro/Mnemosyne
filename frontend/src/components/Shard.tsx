import type { SearchHit } from "../types";

export function Shard({ hit, index }: { hit: SearchHit; index: number }) {
  return (
    <article
      className="parchment rise rounded-sm border border-gold/20 p-4"
      style={{ animationDelay: `${index * 80}ms` }}
    >
      <div className="mb-2 flex items-baseline justify-between gap-4">
        <p className="font-display text-[10px] tracking-[0.28em] text-gold uppercase">{hit.title}</p>
        <p className="font-sans text-[10px] tracking-[0.2em] text-ivory/50">{(hit.score * 100).toFixed(0)}% echo</p>
      </div>
      <p className="font-serif text-lg leading-relaxed text-ivory/90">{hit.text}</p>
    </article>
  );
}
