from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import search, chat, images, models, computer, connectors

app = FastAPI(title="FreePerplexity API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(images.router, prefix="/api", tags=["images"])
app.include_router(models.router, prefix="/api", tags=["models"])
app.include_router(computer.router, prefix="/api", tags=["computer"])
app.include_router(connectors.router, prefix="/api", tags=["connectors"])

@app.get("/")
async def root():
    return {"ok": True, "service": "free-perplexity", "searxng": settings.searxng_candidates}

@app.get("/health")
async def health():
    return {"ok": True}
