import httpx
from bs4 import BeautifulSoup

TIMEOUT = httpx.Timeout(12.0, connect=5.0)

async def fetch_page_text(url: str, max_chars: int = 6000) -> str:
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0 (FreePerplexity)"}) as c:
            r = await c.get(url)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "lxml")
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            text = " ".join(soup.get_text(separator=" ").split())
            return text[:max_chars]
    except Exception as e:
        return f"[fetch failed: {e}]"

async def fetch_og_image(url: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0"}) as c:
            r = await c.get(url)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "lxml")
            tag = soup.find("meta", property="og:image") or soup.find("meta", attrs={"name": "twitter:image"})
            return tag.get("content", "") if tag else ""
    except Exception:
        return ""
