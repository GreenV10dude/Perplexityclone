from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
import httpx

router = APIRouter()

@router.get("/image")
async def image_proxy(url: str = Query(...)):
    """Proxy thumbnails to avoid hotlink/CORS breakage. Streams bytes through."""
    async def gen():
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0"}) as c:
            async with c.stream("GET", url) as r:
                ctype = r.headers.get("content-type", "")
                if "image" not in ctype and "octet" not in ctype:
                    return
                async for chunk in r.aiter_bytes(65536):
                    yield chunk
    return StreamingResponse(gen(), media_type="image/jpeg", headers={"Cache-Control": "public, max-age=86400"})
