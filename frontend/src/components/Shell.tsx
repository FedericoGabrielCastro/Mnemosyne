import { Link, NavLink } from "react-router-dom";
import type { ReactNode } from "react";
import { Starfield } from "./Starfield";

export function Shell({ children }: { children: ReactNode }) {
  return (
    <div className="palace-bg relative min-h-svh">
      <Starfield />
      <div className="relative z-10">
        <header className="flex items-center justify-between px-6 py-5 md:px-10">
          <Link to="/" className="group flex items-center gap-3">
            <span className="grid h-10 w-10 place-items-center rounded-full border border-gold/40 bg-void/60 font-display text-lg text-gold-bright">
              M
            </span>
            <span>
              <span className="block font-display text-sm tracking-[0.42em] text-gold-bright">MNEMOSYNE</span>
              <span className="block font-serif text-sm italic text-ivory/60">the river that remembers</span>
            </span>
          </Link>
          <nav className="flex gap-6 font-sans text-xs tracking-[0.28em] uppercase text-ivory/70">
            <NavLink to="/" className={({ isActive }) => (isActive ? "text-gold-bright" : "hover:text-gold")}>
              Gate
            </NavLink>
            <NavLink to="/vaults" className={({ isActive }) => (isActive ? "text-gold-bright" : "hover:text-gold")}>
              Vaults
            </NavLink>
          </nav>
        </header>
        <div className="river mx-6 md:mx-10" />
        {children}
      </div>
    </div>
  );
}
