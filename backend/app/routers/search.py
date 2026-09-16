from fastapi import APIRouter, Query
from ..services.searxng import searxng_search, search_both

router = APIRouter()

@router.get("/search")
async def search(q: str = Query(...), categories: str = "general", pageno: int = 1):
    try:
        results, inst = await searxng_search(q, categories, pageno)
        return {"query": q, "instance": inst, "results": results}
    except Exception as e:
        return {"query": q, "instance": f"unavailable: {e}", "results": [], "error": str(e)}

@router.get("/search-all")
async def search_all(q: str = Query(...)):
    """Always-on: web + images together."""
    try:
        general, images, inst = await search_both(q)
        return {"query": q, "instance": inst, "results": general, "images": images}
    except Exception as e:
        return {"query": q, "instance": f"unavailable: {e}", "results": [], "images": [], "error": str(e)}
