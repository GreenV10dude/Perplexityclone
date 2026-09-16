# FreePerplexity — free BYOK Perplexity clone

Claude-like UI + unlimited SearXNG search (no search API key) + your own LLM key (20 providers via LiteLLM).

## Quick start (no Docker)
```bash
cp .env.example .env
python3 -m pip install -r backend/requirements.txt
SEARXNG_URL=http://localhost:8888 python3 -m uvicorn backend.app.main:app --port 8000 &
cd frontend && npm install && NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
# open http://localhost:3000, add key in ⚙ Settings
```

## With Docker (bundled unlimited search)
```bash
docker compose up --build
# web http://localhost:3000, api http://localhost:8000, searxng http://localhost:8888
```

## Layout
- Prompt on top, answer text directly below, **thumbnail rail always on the right** (images for every query).
- `GET /api/search-all?q=` returns web + images together.
- `POST /api/chat` streams SSE: `meta` (images+sources) first, then `token`s.
- BYOK: OpenAI, Anthropic, Gemini, xAI, DeepSeek, Mistral, Cohere, Groq, Together, Fireworks, OpenRouter, HF, Qwen, Zhipu, Kimi, Nvidia, Azure, Bedrock, Vertex, Ollama.

## Computer (multi-agent runner)
- Switch to **Computer** mode in the UI. Planner decomposes task → parallel researcher/fetcher → coder in per-task sandbox → writer deliverable.
- `POST /api/computer/stream` streams `task_started → plan → step_started/done → file → done`. `POST /api/computer` runs to completion as JSON.
- Tasks: `GET /api/computer/tasks`, `GET /api/computer/tasks/{id}`, `POST /api/computer/tasks/{id}/cancel`, files at `.../files` + `.../download?name=REPORT.md`.
- Sandbox: one workspace per task under `/tmp/freeplexity_tasks/{id}` (REPORT.md, agent_code.py, outputs). Works with no key via heuristic planner + fallback coder.
- Schedules: `POST /api/computer/schedule` (stored, trigger manually for now).

## Connectors (55 apps)
- Click **🔌 Connectors** in the sidebar: all 10 sections — Popular, Developer, Productivity, Data & Analytics, Operations, Sales & Marketing, Creative, Finance, New, Health — including Gmail with Calendar, Outlook, HubSpot, Mailchimp, Monday.com, Supabase, Neon, Todoist, Cal.com, ClickUp, Atlassian, Shopify, Apollo.io, Klaviyo, Figma, Canva Enterprise, Twitch, IBKR, D&B, AngelList, Evernote, Benchling, Hugging Face, GitHub, Slack, Notion + more.
- Link apps (stored in browser localStorage only), optionally add a per-app API key or MCP server URL, and **Run action** to test it.
- Linked app ids are sent with chat (`POST /api/chat {connectors: [...]}`) and Computer runs so answers can use them.
- API: `GET /api/connectors` (grouped catalog), `GET /api/connectors/{id}`, `POST /api/connectors/execute` `{connector_id, action, params, credential, mcp_url}`. Without credentials it returns labeled demo data; with `mcp_url` it proxies to your MCP server.

## Push to GitHub + host the site (Actions → Pages)
```bash
cd /Users/ishansathish/Desktop/Perplexity
git init -b main
git add -A && git commit -m "FreePerplexity: chat + computer + 55 connectors"
gh repo create freeplexity --public --source=. --push
# Then: repo Settings → Pages → Source: GitHub Actions
```
- The workflow `.github/workflows/deploy.yml` builds `frontend/` (`output: export`) and deploys `frontend/out` to Pages on every push to `main`. No backend needed — the site runs in demo mode offline.
- For **live** search on the hosted site: deploy the backend (Render one-click via `render.yaml`, Railway, or any VPS with `docker compose up`), then set repo secret `API_URL` to the backend URL and re-run the workflow (`NEXT_PUBLIC_API_URL` is baked at build time).
- Project pages (`user.github.io/<repo>`) need base path: set repo variable `NEXT_BASE_PATH=/<repo>` (user/org sites use root, leave empty).
