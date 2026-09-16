"""Tiny memory: per-task summaries + global notes (JSON on disk)."""
import json
import os
import tempfile

MEM_PATH = os.path.join(tempfile.gettempdir(), "freeplexity_tasks", "_memory.json")

def _load() -> dict:
    try:
        with open(MEM_PATH) as f:
            return json.load(f)
    except Exception:
        return {"notes": []}

def _save(m: dict):
    os.makedirs(os.path.dirname(MEM_PATH), exist_ok=True)
    with open(MEM_PATH, "w") as f:
        json.dump(m, f)

def remember(summary: str):
    m = _load()
    m["notes"].append(summary[:2000])
    m["notes"] = m["notes"][-50:]
    _save(m)

def recall(limit: int = 5) -> list[str]:
    return _load().get("notes", [])[-limit:]
