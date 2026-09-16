"""Runner: executes plan, streams events. Parallel where independent."""
import asyncio
import time
from .store import get_task
from .planner import plan_task
from . import agents, sandbox
from .memory import remember

async def run_task(task_id: str, task: str, provider: str, model: str, api_key: str):
    """Async generator of event dicts."""
    t = get_task(task_id)
    if not t:
        yield {"type": "error", "text": "task not found"}
        return
    t["status"] = "planning"
    yield {"type": "task_started", "id": task_id, "task": task}

    steps, planner_used = await plan_task(task, provider, model, api_key)
    t["plan"] = steps
    for s in steps:
        t["steps"][s["id"]] = {**s, "status": "pending", "log": [], "result": {}}
    yield {"type": "plan", "steps": steps, "planner": planner_used}

    if t.get("cancel"):
        t["status"] = "cancelled"
        yield {"type": "done", "status": "cancelled"}
        return

    # Run non-writer steps (parallel in groups: researchers/fetchers together, then coder)
    parallel_ids = [s["id"] for s in steps if s["agent"] in ("researcher", "fetcher")]
    coder_ids = [s["id"] for s in steps if s["agent"] == "coder"]
    writer_steps = [s for s in steps if s["agent"] == "writer"]

    async def run_one(sid: str):
        st = t["steps"][sid]
        if t.get("cancel"):
            st["status"] = "cancelled"
            return st
        st["status"] = "running"
        try:
            if st["agent"] == "researcher":
                res = await agents.researcher(st["prompt"], provider, model, api_key)
            elif st["agent"] == "fetcher":
                res = await agents.fetcher(st["prompt"], provider, model, api_key)
            elif st["agent"] == "coder":
                res = await agents.coder(task_id, st["prompt"], provider, model, api_key)
            else:
                res = {"text": "skipped"}
            st["result"] = res
            st["status"] = "done"
            # accumulate sources/images/files
            t["sources"].extend(res.get("sources", []))
            if res.get("images"):
                t["images"].extend(res["images"])
            for f in res.get("files", []):
                if f["name"] not in [x["name"] for x in t["files"]]:
                    t["files"].append(f)
        except Exception as e:
            st["status"] = "error"
            st["result"] = {"text": f"error: {e}"}
        return st

    t["status"] = "running"
    # phase 1: research/fetch parallel
    if parallel_ids:
        for sid in parallel_ids:
            t["steps"][sid]["status"] = "running"
            yield {"type": "step_started", "id": sid, "step": t["steps"][sid]}
        done = await asyncio.gather(*[run_one(sid) for sid in parallel_ids])
        for st in done:
            yield {"type": "step_done", "id": st["id"], "step": _public(st)}
            if t.get("cancel"):
                break
    # phase 2: coder(s) sequential (share filesystem)
    for sid in coder_ids:
        if t.get("cancel"):
            t["steps"][sid]["status"] = "cancelled"
            yield {"type": "step_done", "id": sid, "step": _public(t["steps"][sid])}
            continue
        yield {"type": "step_started", "id": sid, "step": _public(t["steps"][sid])}
        st = await run_one(sid)
        yield {"type": "step_done", "id": sid, "step": _public(st)}
        for f in st.get("result", {}).get("files", []):
            yield {"type": "file", "file": f}

    if t.get("cancel"):
        t["status"] = "cancelled"
        yield {"type": "done", "status": "cancelled"}
        return

    # phase 3: writer
    gathered = [{"agent": t["steps"][s["id"]]["agent"], "title": t["steps"][s["id"]]["title"], "result": t["steps"][s["id"]].get("result", {})}
                for s in steps if t["steps"][s["id"]].get("status") == "done"]
    for w in writer_steps:
        t["steps"][w["id"]]["status"] = "running"
        yield {"type": "step_started", "id": w["id"], "step": _public(t["steps"][w["id"]])}
        try:
            res = await agents.writer(task_id, task, gathered, provider, model, api_key)
            t["steps"][w["id"]]["result"] = res
            t["steps"][w["id"]]["status"] = "done"
            t["final"] = res["text"]
            for f in res.get("files", []):
                if f["name"] not in [x["name"] for x in t["files"]]:
                    t["files"].append(f)
                    yield {"type": "file", "file": f}
        except Exception as e:
            t["steps"][w["id"]]["status"] = "error"
            t["steps"][w["id"]]["result"] = {"text": str(e)}
        yield {"type": "step_done", "id": w["id"], "step": _public(t["steps"][w["id"]])}

    # dedupe sources
    seen, uniq = set(), []
    for s in t["sources"]:
        u = s.get("url", "")
        if u and u not in seen:
            seen.add(u)
            uniq.append(s)
    t["sources"] = uniq[:20]
    t["files"] = sandbox.list_files(task_id)
    t["status"] = "done"
    try:
        remember(f"{task} -> {t['final'][:500]}")
    except Exception:
        pass
    yield {"type": "done", "status": "done", "final": t["final"], "sources": t["sources"], "images": t["images"][:9], "files": t["files"]}

def _public(st: dict) -> dict:
    r = st.get("result", {})
    return {"id": st["id"], "agent": st["agent"], "title": st["title"], "status": st["status"],
            "text": (r.get("text", "") or "")[:3000],
            "sources": r.get("sources", [])[:6], "images": r.get("images", [])[:6],
            "files": r.get("files", []), "exec": r.get("exec")}
