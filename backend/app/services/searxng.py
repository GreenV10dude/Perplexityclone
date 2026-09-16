import asyncio
import hashlib
import httpx
from urllib.parse import urlparse
from ..config import settings

TIMEOUT = httpx.Timeout(10.0, connect=5.0)
_mem_cache: dict[str, dict] = {}

def _cache_key(q: str, categories: str, pageno: int) -> str:
    return hashlib.md5(f"{q}|{categories}|{pageno}".encode()).hexdigest()

async def _query_one(client: httpx.AsyncClient, base: str, q: str, categories: str, pageno: int, time_range: str = "") -> list[dict]:
    params = {"q": q, "format": "json", "categories": categories, "pageno": pageno, "language": "en"}
    if time_range:
        params["time_range"] = time_range
    r = await client.get(f"{base}/search", params=params)
    r.raise_for_status()
    data = r.json()
    return data.get("results", [])

async def searxng_search(q: str, categories: str = "general", pageno: int = 1, time_range: str = "", max_results: int = 10) -> tuple[list[dict], str]:
    """Try bundled SearXNG first, then public fallbacks. Returns (results, used_instance)."""
    key = _cache_key(q, categories, pageno)
    if key in _mem_cache:
        hit = _mem_cache[key]
        return hit["results"][:max_results], hit["instance"] + " (cache)"
    last_err = "no instances configured"
    async with httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0 (FreePerplexity)"}) as client:
        for base in settings.searxng_candidates:
            try:
                raw = await _query_one(client, base, q, categories, pageno, time_range)
                norm = [normalize(r) for r in raw[:max_results]]
                _mem_cache[key] = {"results": norm, "instance": base}
                return norm, base
            except Exception as e:
                last_err = f"{base}: {e}"
                continue
    raise RuntimeError(f"All SearXNG instances failed. Last error: {last_err}")

def normalize(r: dict) -> dict:
    url = r.get("url", "")
    try:
        domain = urlparse(url).netloc
    except Exception:
        domain = ""
    return {
        "title": r.get("title", "")[:200],
        "url": url,
        "snippet": (r.get("content") or "")[:600],
        "domain": domain,
        "engine": r.get("engine", ""),
        "img_src": r.get("img_src", "") or r.get("thumbnail", ""),
    }

async def search_both(q: str) -> tuple[list[dict], list[dict], str]:
    """ALWAYS-ON: general + images in parallel for every query."""
    (general, inst), (images, _) = await asyncio.gather(
        searxng_search(q, "general", max_results=10),
        searxng_search(q, "images", max_results=10),
    )
    # dedupe images by img_src
    seen, uniq_images = set(), []
    for im in images:
        src = im.get("img_src") or im.get("url")
        if not src or src in seen:
            continue
        seen.add(src)
        uniq_images.append({
            "thumb": src,
            "full": im.get("url", src),
            "title": im.get("title", ""),
            "source": im.get("domain", ""),
            "source_url": im.get("url", ""),
        })
    return general, uniq_images[:9], inst
