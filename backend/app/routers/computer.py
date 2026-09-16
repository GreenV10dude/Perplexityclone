import json
import time
import uuid
from fastapi import APIRouter
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from ..services.computer.store import create_task, get_task, list_tasks, TASKS, SCHEDULES
from ..services.computer.runner import run_task
from ..services.computer import sandbox

router = APIRouter()

class ComputerReq(BaseModel):
    task: str
    provider: str = "openai"
    model: str = "gpt-4o-mini"
    api_key: str = ""
    base_url: str = ""
    connectors: list[str] = []

class ScheduleReq(BaseModel):
    task: str
    every_seconds: int = 3600
    provider: str = "openai"
    model: str = "gpt-4o-mini"
    api_key: str = ""

def _sse(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"

@router.post("/computer/stream")
async def computer_stream(req: ComputerReq):
    t = create_task(req.task, req.provider, req.model)
    try:
        from ..services.llm import apply_byok
        apply_byok(req.provider, req.api_key, req.base_url)
    except Exception:
        pass
    from ..services.connectors_catalog import connector_context
    note = connector_context(req.connectors)
    effective = req.task + ("\n\n" + note if note else "")

    async def gen():
        async for ev in run_task(t["id"], effective, req.provider, req.model, req.api_key):
            yield _sse(ev)

    return StreamingResponse(gen(), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

@router.post("/computer")
async def computer_run(req: ComputerReq):
    """Non-streaming: run to completion, return JSON."""
    t = create_task(req.task, req.provider, req.model)
    from ..services.connectors_catalog import connector_context
    note = connector_context(req.connectors)
    effective = req.task + ("\n\n" + note if note else "")
    final_ev: dict = {}
    async for ev in run_task(t["id"], effective, req.provider, req.model, req.api_key):
        if ev.get("type") == "done":
            final_ev = ev
    task = get_task(t["id"])
    return {"id": t["id"], "status": task["status"], "final": task["final"],
            "sources": task["sources"], "images": task["images"][:9],
            "files": task["files"], "steps": list(task["steps"].values())}

@router.get("/computer/tasks")
async def computer_tasks():
    return {"tasks": [
        {"id": x["id"], "task": x["task"], "status": x["status"], "created_at": x["created_at"],
         "files": len(x["files"]), "steps": len(x["steps"])} for x in list_tasks()]}

@router.get("/computer/tasks/{tid}")
async def computer_get(tid: str):
    t = get_task(tid)
    if not t:
        return {"error": "not found"}
    return {"id": t["id"], "task": t["task"], "status": t["status"], "plan": t["plan"],
            "steps": list(t["steps"].values()), "final": t["final"],
            "sources": t["sources"], "images": t["images"][:9], "files": t["files"]}

@router.post("/computer/tasks/{tid}/cancel")
async def computer_cancel(tid: str):
    t = get_task(tid)
    if not t:
        return {"error": "not found"}
    t["cancel"] = True
    return {"ok": True, "id": tid}

@router.get("/computer/tasks/{tid}/files")
async def computer_files(tid: str):
    t = get_task(tid)
    if not t:
        return {"error": "not found"}
    return {"files": sandbox.list_files(tid)}

@router.get("/computer/tasks/{tid}/download")
async def computer_download(tid: str, name: str):
    p = sandbox._safe_join(tid, name)
    return FileResponse(p, filename=name)

@router.get("/computer/memory")
async def computer_memory():
    from ..services.computer.memory import recall
    return {"notes": recall(10)}

# Scheduled recurring tasks (MVP: store + manual trigger; APScheduler upgrade path)
@router.post("/computer/schedule")
async def computer_schedule(req: ScheduleReq):
    sid = uuid.uuid4().hex[:8]
    SCHEDULES[sid] = {"id": sid, **req.model_dump(), "created_at": time.time(), "last_run": None}
    return {"ok": True, "schedule": SCHEDULES[sid]}

@router.get("/computer/schedule")
async def computer_schedules():
    return {"schedules": list(SCHEDULES.values())}
