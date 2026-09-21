# Mnemosyne web

Extravagant oracle for the local memory palace. Vite, React, pnpm, Tailwind.

## Run

```bash
cd frontend
pnpm install
pnpm dev
```

The Vite server proxies `/api` to Django on `http://127.0.0.1:8000`. Open `http://127.0.0.1:5173`.

Optional: `VITE_API_URL=http://127.0.0.1:8000` if you are not using the proxy.
