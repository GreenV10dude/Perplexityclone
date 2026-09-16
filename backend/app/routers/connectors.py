from fastapi import APIRouter
from pydantic import BaseModel
from ..services.connectors_catalog import CONNECTORS, SECTIONS, grouped, BY_ID, execute

router = APIRouter()

@router.get("/connectors")
async def list_connectors():
    return {"sections": SECTIONS, "grouped": grouped(),
            "total": len(CONNECTORS),
            "connectors": [{"id": c["id"], "label": c["label"], "sections": c["sections"],
                            "auth": c["auth"], "desc": c["desc"], "actions": c["actions"],
                            "key_hint": c["key_hint"]} for c in CONNECTORS]}

@router.get("/connectors/{cid}")
async def connector_detail(cid: str):
    c = BY_ID.get(cid)
    if not c:
        return {"error": "not found"}
    return c

class ExecReq(BaseModel):
    connector_id: str
    action: str
    params: dict = {}
    credential: str = ""  # BYOK per-connector; never stored server-side
    mcp_url: str = ""     # optional MCP server to proxy through

@router.post("/connectors/execute")
async def connector_execute(req: ExecReq):
    return await execute(req.connector_id, req.action, req.params, req.credential, req.mcp_url)
