"""Filesystem sandbox: one workspace dir per task. Safe path handling + code exec."""
import os
import pathlib
import subprocess
import sys
import tempfile

ROOT = os.path.join(tempfile.gettempdir(), "freeplexity_tasks")
os.makedirs(ROOT, exist_ok=True)

def workspace(task_id: str) -> str:
    d = os.path.join(ROOT, task_id)
    os.makedirs(d, exist_ok=True)
    return d

def _safe_join(task_id: str, name: str) -> str:
    ws = workspace(task_id)
    p = os.path.normpath(os.path.join(ws, name))
    if not p.startswith(ws):
        raise ValueError("path traversal blocked")
    return p

def write_file(task_id: str, name: str, content: str) -> dict:
    p = _safe_join(task_id, name)
    os.makedirs(os.path.dirname(p) or workspace(task_id), exist_ok=True)
    with open(p, "w") as f:
        f.write(content)
    return {"name": name, "path": p, "size": len(content)}

def read_file(task_id: str, name: str, max_chars: int = 20000) -> str:
    p = _safe_join(task_id, name)
    with open(p) as f:
        return f.read()[:max_chars]

def list_files(task_id: str) -> list[dict]:
    ws = workspace(task_id)
    out = []
    for root, _, files in os.walk(ws):
        for fn in files:
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, ws)
            try:
                out.append({"name": rel, "size": os.path.getsize(fp)})
            except OSError:
                pass
    return out

def run_python(task_id: str, code: str, timeout: int = 20) -> dict:
    """Run python snippet inside task workspace cwd. Returns stdout/stderr."""
    ws = workspace(task_id)
    script = _safe_join(task_id, "_agent_run.py")
    with open(script, "w") as f:
        f.write(code)
    try:
        proc = subprocess.run(
            [sys.executable, script],
            cwd=ws, capture_output=True, text=True, timeout=timeout,
        )
        return {"ok": proc.returncode == 0, "stdout": proc.stdout[-6000:], "stderr": proc.stderr[-3000:], "code": proc.returncode}
    except subprocess.TimeoutExpired:
        return {"ok": False, "stdout": "", "stderr": f"timeout after {timeout}s", "code": -1}
    except Exception as e:
        return {"ok": False, "stdout": "", "stderr": str(e), "code": -1}

def run_shell(task_id: str, cmd: str, timeout: int = 20) -> dict:
    ws = workspace(task_id)
    try:
        proc = subprocess.run(cmd, shell=True, cwd=ws, capture_output=True, text=True, timeout=timeout)
        return {"ok": proc.returncode == 0, "stdout": proc.stdout[-6000:], "stderr": proc.stderr[-3000:], "code": proc.returncode}
    except subprocess.TimeoutExpired:
        return {"ok": False, "stdout": "", "stderr": f"timeout after {timeout}s", "code": -1}
