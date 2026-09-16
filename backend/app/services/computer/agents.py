"""Sub-agents: researcher / fetcher / coder / writer. All work without a key (extractive fallback)."""
import asyncio
import re
from ..searxng import searxng_search, search_both
from ..scraper import fetch_page_text
from ..llm import SYNTHESIZE, build_context, litellm_model, apply_byok
from . import sandbox

async def _llm(prompt_sys: str, prompt_user: str, provider: str, model: str, api_key: str, max_tokens: int = 1500) -> str | None:
    if not api_key and provider != "ollama":
        return None
    try:
        from litellm import acompletion
        apply_byok(provider, api_key)
        resp = await acompletion(
            model=litellm_model(provider, model),
            messages=[{"role": "system", "content": prompt_sys}, {"role": "user", "content": prompt_user}],
            temperature=0.3, max_tokens=max_tokens,
        )
        return resp.choices[0].message.content or ""
    except Exception as e:
        return f"[llm error: {e}]"

async def researcher(prompt: str, provider: str, model: str, api_key: str) -> dict:
    general, images, inst = [], [], "unavailable"
    try:
        general, images, inst = await search_both(prompt[:300])
    except Exception as e:
        inst = f"search failed: {e}"
    context = build_context(general)
    text = await _llm(SYNTHESIZE, f"TASK: {prompt}\n\nSOURCES:\n{context}", provider, model, api_key)
    if text is None:
        lines = [f"Top sources for: {prompt} (extractive, add key for synthesis)\n"]
        for i, r in enumerate(general[:6], 1):
            lines.append(f"[{i}] {r['title']} ({r['domain']})\n{r['snippet']}\n{r['url']}\n")
        text = "\n".join(lines) if general else "No web results (SearXNG not running). Start bundled SearXNG via docker compose."
    return {"text": text, "sources": general, "images": images, "instance": inst}

async def fetcher(prompt: str, provider: str, model: str, api_key: str) -> dict:
    urls = re.findall(r"https?://\S+", prompt)
    if not urls:
        # try one search to discover a URL
        try:
            general, _, _ = await search_both(prompt[:200])
            urls = [r["url"] for r in general[:3]]
        except Exception:
            pass
    texts = await asyncio.gather(*[fetch_page_text(u) for u in urls[:4]])
    joined = "\n\n".join(f"URL {u}:\n{t[:3000]}" for u, t in zip(urls, texts))
    summary = await _llm("Summarize fetched pages concisely with key facts.", f"TASK: {prompt}\n\n{joined}", provider, model, api_key)
    if summary is None:
        summary = joined[:4000] or "Nothing fetched."
    return {"text": summary, "sources": [{"title": u, "url": u, "domain": u.split('/')[2] if '/' in u else u, "snippet": t[:300]} for u, t in zip(urls, texts)], "images": [], "instance": "fetch"}

async def coder(task_id: str, prompt: str, provider: str, model: str, api_key: str) -> dict:
    code = None
    gen = await _llm(
        "You write minimal runnable python. Output ONLY code, no markdown fences.",
        f"Write python that accomplishes: {prompt}\nSave any artifact to the cwd (e.g. output.csv, app.py, index.html). Print key results.",
        provider, model, api_key, max_tokens=1500)
    if gen and "llm error" not in gen:
        code = gen.strip().strip("`")
        if code.startswith("python"):
            code = code.split("\n", 1)[1] if "\n" in code else code
    if not code:
        # deterministic fallback so Computer is useful with $0 / no key
        code = (
            "import json, datetime\n"
            f"TASK = {prompt!r}\n"
            "print('Task:', TASK)\n"
            "print('Ran at:', datetime.datetime.utcnow().isoformat())\n"
            "with open('output.json','w') as f:\n"
            "    json.dump({'task': TASK, 'status': 'fallback-run-ok'}, f, indent=2)\n"
            "print('Wrote output.json')\n"
        )
    sandbox.write_file(task_id, "agent_code.py", code)
    res = sandbox.run_python(task_id, code)
    files = sandbox.list_files(task_id)
    out_text = f"Ran agent_code.py (exit {res['code']}).\nSTDOUT:\n{res['stdout']}\nSTDERR:\n{res['stderr']}"
    return {"text": out_text, "code": code, "exec": res, "sources": [], "images": [], "instance": "sandbox", "files": files}

async def writer(task_id: str, original_task: str, gathered: list[dict], provider: str, model: str, api_key: str) -> dict:
    combined = "\n\n".join(f"--- {g.get('title', g.get('agent',''))} ---\n{g.get('result',{}).get('text','')[:4000]}" for g in gathered)
    final = await _llm(SYNTHESIZE, f"ORIGINAL TASK: {original_task}\n\nSUB-AGENT OUTPUTS:\n{combined}\n\nWrite the final deliverable with citations.", provider, model, api_key, max_tokens=2500)
    if final is None:
        final = f"# Result: {original_task}\n\n" + combined[:6000] + "\n\n_Add a BYOK key for polished synthesis._"
    sandbox.write_file(task_id, "REPORT.md", final)
    files = sandbox.list_files(task_id)
    return {"text": final, "sources": [], "images": [], "instance": "writer", "files": files}
