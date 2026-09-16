from fastapi import APIRouter
from ..services.providers import PROVIDERS

router = APIRouter()

@router.get("/models")
async def models():
    return {"providers": PROVIDERS}
