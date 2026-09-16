import sys
sys.path.insert(0, ".")
from backend.app.services.llm import build_context, litellm_model
from backend.app.services.providers import PROVIDERS

# 1. providers = 20
assert len(PROVIDERS) == 20, f"expected 20 providers, got {len(PROVIDERS)}"
# 2. context builder cites [1]
ctx = build_context([{"title": "T", "domain": "d.com", "url": "http://d.com", "snippet": "s"}])
assert "[1]" in ctx
# 3. litellm mapping
assert litellm_model("gemini", "gemini-2.5-flash") == "gemini/gemini-2.5-flash"
assert litellm_model("openai", "gpt-4o-mini") == "gpt-4o-mini"
# 4. FastAPI routes mounted
from backend.app.main import app
paths = set(app.openapi()["paths"].keys())
for p in ["/api/search", "/api/search-all", "/api/chat", "/api/image", "/api/models",
          "/api/computer", "/api/computer/stream", "/api/computer/tasks",
          "/api/computer/tasks/{tid}", "/api/computer/tasks/{tid}/cancel",
          "/api/computer/tasks/{tid}/files", "/api/computer/schedule",
          "/api/connectors", "/api/connectors/{cid}", "/api/connectors/execute"]:
    assert p in paths, f"missing {p}"
print("ALL CHECKS PASSED: 20 providers, citations, 6 routes")

# 5. Computer planner + sandbox
from backend.app.services.computer.planner import heuristic_plan
from backend.app.services.computer import sandbox as sb
steps = heuristic_plan("Build a python script that analyzes data")
assert steps[0]["agent"] == "researcher" and steps[-1]["agent"] == "writer"
assert any(s["agent"] == "coder" for s in steps)
r = sb.run_python("verify-task", "print('hello-computer')")
assert r["ok"] and "hello-computer" in r["stdout"], r
print("COMPUTER CHECKS PASSED: planner + sandbox exec")

# 6. Connectors catalog
import asyncio
from backend.app.services.connectors_catalog import CONNECTORS, SECTIONS, grouped, connector_context, execute, BY_ID
assert len(SECTIONS) == 10, SECTIONS
assert len(CONNECTORS) >= 51, len(CONNECTORS)
for required in ["gmail-calendar", "outlook", "hubspot", "mailchimp", "monday", "supabase",
                 "neon", "todoist", "clickup", "atlassian", "shopify", "apollo", "figma",
                 "ibkr", "dnb", "evernote", "benchling", "huggingface"]:
    assert required in BY_ID, f"missing {required}"
assert "HubSpot" in connector_context(["hubspot", "gmail-calendar"])
assert connector_context([]) == ""
res = asyncio.run(execute("hubspot", "search_contacts", {"query": "acme"}))
assert res["ok"] and res["demo"] and res["result"]["count"] == 3
bad = asyncio.run(execute("nope", "x", {}))
assert not bad["ok"]
print(f"CONNECTORS CHECKS PASSED: {len(CONNECTORS)} apps, 10 sections, execute demo")
