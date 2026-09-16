"""Planner: LLM decomposition with heuristic fallback (works with no key)."""
import json
import re

PLANNER_SYS = """Decompose the user task into 3-6 executable subtasks for sub-agents.
Agents available: researcher (web search + citations), fetcher (read specific URLs/pages),
coder (write+run python in sandbox, analyze data, build artifacts), writer (final cited deliverable).
Return ONLY JSON: [{"id":"s1","agent":"researcher","title":"...","prompt":"..."}, ...]
Keep prompts self-contained. Researcher steps can run in parallel. Writer always last."""

def heuristic_plan(task: str) -> list[dict]:
    t = task.lower()
    urls = re.findall(r"https?://\S+", task)
    steps = [
        {"id": "s1", "agent": "researcher", "title": "Web research", "prompt": f"Research with citations: {task}"},
    ]
    if urls:
        steps.append({"id": "s2", "agent": "fetcher", "title": f"Read {len(urls)} link(s)", "prompt": f"Fetch and summarize these URLs:\n" + "\n".join(urls)})
    needs_code = any(k in t for k in ["code", "app", "website", "script", "analy", "data", "csv", "chart", "plot", "calcul", "scrape", "automat"])
    if needs_code:
        steps.append({"id": "s3", "agent": "coder", "title": "Build / compute in sandbox", "prompt": f"In the sandbox workspace, produce runnable code/analysis for: {task}. Save outputs as files."})
    steps.append({"id": "s4", "agent": "writer", "title": "Final deliverable", "prompt": f"Write the final cited answer/deliverable for: {task}. Save REPORT.md."})
    # renumber
    for i, s in enumerate(steps):
        s["id"] = f"s{i+1}"
    return steps

async def plan_task(task: str, provider: str, model: str, api_key: str) -> tuple[list[dict], str]:
    """Returns (steps, planner_used)."""
    if not api_key and provider != "ollama":
        return heuristic_plan(task), "heuristic (no key)"
    try:
        from litellm import acompletion
        from ..llm import litellm_model, apply_byok
        apply_byok(provider, api_key)
        resp = await acompletion(
            model=litellm_model(provider, model),
            messages=[{"role": "system", "content": PLANNER_SYS}, {"role": "user", "content": task}],
            temperature=0.2, max_tokens=800,
        )
        text = resp.choices[0].message.content or ""
        m = re.search(r"\[.*\]", text, re.S)
        steps = json.loads(m.group(0) if m else text)
        # validate
        clean = []
        for i, s in enumerate(steps[:6]):
            agent = s.get("agent", "researcher") if isinstance(s, dict) else "researcher"
            if agent not in ("researcher", "fetcher", "coder", "writer"):
                agent = "researcher"
            clean.append({"id": f"s{i+1}", "agent": agent,
                          "title": str(s.get("title", agent))[:120] if isinstance(s, dict) else agent,
                          "prompt": str(s.get("prompt", task))[:2000] if isinstance(s, dict) else task})
        if clean and clean[-1]["agent"] != "writer":
            clean.append({"id": f"s{len(clean)+1}", "agent": "writer", "title": "Final deliverable", "prompt": f"Write final cited deliverable for: {task}"})
        return clean, "llm"
    except Exception:
        return heuristic_plan(task), "heuristic (llm error)"
