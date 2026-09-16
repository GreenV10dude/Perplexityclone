"""In-memory task store + on-disk workspace root. Upgrade path: Postgres + S3."""
import time
import uuid

TASKS: dict[str, dict] = {}
SCHEDULES: dict[str, dict] = {}

def new_task_id() -> str:
    return uuid.uuid4().hex[:12]

def create_task(task: str, provider: str, model: str) -> dict:
    tid = new_task_id()
    t = {
        "id": tid,
        "task": task,
        "provider": provider,
        "model": model,
        "status": "queued",
        "created_at": time.time(),
        "plan": [],
        "steps": {},  # step_id -> {id, agent, title, prompt, status, log[], result}
        "files": [],  # {name, path, size}
        "final": "",
        "sources": [],
        "images": [],
        "cancel": False,
    }
    TASKS[tid] = t
    return t

def get_task(tid: str) -> dict | None:
    return TASKS.get(tid)

def list_tasks() -> list[dict]:
    return sorted(TASKS.values(), key=lambda x: x["created_at"], reverse=True)[:50]
