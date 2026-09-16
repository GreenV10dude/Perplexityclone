import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from ..services.searxng import search_both
from ..services.scraper import fetch_page_text
from ..services.llm import SYNTHESIZE, build_context, litellm_model, apply_byok
import asyncio

router = APIRouter()

class ChatReq(BaseModel):
    query: str
    provider: str = "openai"
    model: str = "gpt-4o-mini"
    api_key: str = ""
    base_url: str = ""
    deep: bool = False  # deep-research: fetch top pages full-text
    connectors: list[str] = []  # linked app ids, e.g. ["gmail-calendar", "hubspot"]

@router.post("/chat")
async def chat(req: ChatReq):
    try:
        general, images, inst = await search_both(req.query)
    except Exception as e:
        # Resilient: no SearXNG reachable (e.g. local docker not running yet)
        general, images, inst = [], [], f"search unavailable ({e})"
    context = build_context(general)
    if req.deep:
        texts = await asyncio.gather(*[fetch_page_text(r["url"]) for r in general[:3]])
        context += "\n\nFULL TEXT:\n" + "\n\n".join(texts)

    sources = [{"n": i + 1, **r} for i, r in enumerate(general)]

    from ..services.connectors_catalog import connector_context
    conn_note = connector_context(req.connectors)

    async def stream():
        # Send metadata first so UI can render thumbnails rail immediately
        yield f"data: {json.dumps({'type': 'meta', 'images': images, 'sources': sources, 'instance': inst})}\n\n"
        # If no key, return extractive fallback (still useful, $0)
        if not req.api_key and req.provider != "ollama":
            fallback = "No API key provided — showing top sources extractively.\n\n"
            for s in sources[:5]:
                fallback += f"**[{s['n']}] {s['title']}** — {s['snippet']}\n\n"
            fallback += "\nAdd your key in Settings (any of 20 providers) for full AI synthesis."
            yield f"data: {json.dumps({'type': 'token', 'text': fallback})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return
        try:
            from litellm import acompletion
            apply_byok(req.provider, req.api_key, req.base_url)
            resp = await acompletion(
                model=litellm_model(req.provider, req.model),
                messages=[
                    {"role": "system", "content": SYNTHESIZE},
                    {"role": "user", "content": f"QUESTION: {req.query}\n\nSOURCES:\n{context}" + (f"\n\n{conn_note}" if conn_note else "")},
                ],
                stream=True,
            )
            async for chunk in resp:
                delta = chunk.choices[0].delta.content or ""
                if delta:
                    yield f"data: {json.dumps({'type': 'token', 'text': delta})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'token', 'text': f'\n\n[LLM error: {e} — showing extractive results above.]'})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
