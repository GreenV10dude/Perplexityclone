"use client";
import { useEffect, useMemo, useState } from "react";
import { fetchConnectors, executeConnector } from "../lib/api";
import { CONNECTORS_FALLBACK } from "../lib/connectors-fallback";

export function ConnectorsPanel({ open, onClose, active, setActive, creds, setCreds }) {
  const [groups, setGroups] = useState(CONNECTORS_FALLBACK);
  const [live, setLive] = useState(false);
  const [q, setQ] = useState("");
  const [sel, setSel] = useState(null); // selected connector for detail/run
  const [runParams, setRunParams] = useState('{"query": "demo"}');
  const [runOut, setRunOut] = useState(null);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    if (!open) return;
    fetchConnectors().then((d) => {
      if (d?.grouped?.length) { setGroups(d.grouped); setLive(true); }
    }).catch(() => {});
  }, [open ]);

  const filtered = useMemo(() => {
    if (!q.trim()) return groups;
    const needle = q.toLowerCase();
    return groups.map((g) => ({
      ...g,
      connectors: g.connectors.filter((c) =>
        c.label.toLowerCase().includes(needle) || c.desc.toLowerCase().includes(needle)),
    })).filter((g) => g.connectors.length);
  }, [groups, q ]);

  if (!open) return null;
  const total = groups.reduce((n, g) => n + g.connectors.length, 0);

  function toggle(id) {
    setActive((a) => (a.includes(id) ? a.filter((x) => x !== id) : [...a, id]));
  }

  async function runAction() {
    if (!sel) return;
    setRunning(true); setRunOut(null);
    try {
      const out = await executeConnector({
        connector_id: sel.id,
        action: sel.action || sel.actions[0],
        params: JSON.parse(runParams || "{}"),
        credential: creds[sel.id]?.key || "",
        mcp_url: creds[sel.id]?.mcp || "",
      });
      setRunOut(out);
    } catch (e) {
      setRunOut({ ok: false, error: String(e) });
    }
    setRunning(false);
  }

  return (
    <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-[#faf9f6] rounded-2xl w-full max-w-4xl max-h-[85vh] flex flex-col overflow-hidden" onClick={(e) => e.stopPropagation()}>
        <div className="p-4 border-b border-stone-200">
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-semibold">Connectors</h2>
            <span className="text-xs text-stone-500">{total} apps · {active.length} linked{live ? "" : " · offline catalog"}</span>
            <button onClick={onClose} className="ml-auto border rounded-lg px-3 py-1 text-sm bg-white">Close</button>
          </div>
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search apps… (e.g. hubspot, figma, ibkr)"
            className="mt-3 w-full rounded-xl border border-stone-300 bg-white px-4 py-2 text-sm outline-none" />
        </div>
        <div className="flex-1 overflow-y-auto p-4 grid gap-6 md:grid-cols-[1fr_280px]">
          <div className="space-y-6 min-w-0">
            {filtered.map((g) => (
              <div key={g.section}>
                <div className="text-xs font-semibold uppercase tracking-wide text-stone-500 mb-2">{g.section}</div>
                <div className="grid gap-2 sm:grid-cols-2">
                  {g.connectors.map((c) => {
                    const on = active.includes(c.id);
                    return (
                      <div key={c.id} className={`rounded-xl border p-3 bg-white ${on ? "border-stone-900" : "border-stone-200"}`}>
                        <div className="flex items-center gap-2">
                          <button onClick={() => setSel(c)} className="font-medium text-sm text-left hover:underline">{c.label}</button>
                          <span className="text-[10px] text-stone-400">{c.auth}</span>
                          <button onClick={() => toggle(c.id)}
                            className={`ml-auto text-xs rounded-full px-3 py-1 border ${on ? "bg-stone-900 text-white" : "bg-white"}`}>
                            {on ? "Linked ✓" : "Link"}
                          </button>
                        </div>
                        <div className="text-xs text-stone-500 mt-1">{c.desc}</div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
          <aside className="rounded-xl border border-stone-200 bg-white p-3 h-fit md:sticky md:top-0">
            {!sel ? (
              <div className="text-sm text-stone-500">Select an app to see actions, add a key, or run a demo action.</div>
            ) : (
              <div className="space-y-3">
                <div className="font-semibold text-sm">{sel.label}</div>
                <div className="text-xs text-stone-500">{sel.desc}</div>
                <label className="block text-xs">Action
                  <select value={sel.action || sel.actions[0]}
                    onChange={(e) => setSel({ ...sel, action: e.target.value })}
                    className="mt-1 w-full border rounded-lg p-1.5 text-sm">
                    {sel.actions.map((a) => <option key={a} value={a}>{a}</option>)}
                  </select>
                </label>
                <label className="block text-xs">API key / token (optional, stays in browser)
                  <input type="password" value={creds[sel.id]?.key || ""}
                    onChange={(e) => setCreds({ ...creds, [sel.id]: { ...creds[sel.id], key: e.target.value } })}
                    placeholder={sel.key_hint} className="mt-1 w-full border rounded-lg p-1.5 text-sm" />
                </label>
                <label className="block text-xs">MCP server URL (optional)
                  <input value={creds[sel.id]?.mcp || ""}
                    onChange={(e) => setCreds({ ...creds, [sel.id]: { ...creds[sel.id], mcp: e.target.value } })}
                    placeholder="https://…/mcp" className="mt-1 w-full border rounded-lg p-1.5 text-sm" />
                </label>
                <label className="block text-xs">Params (JSON)
                  <textarea value={runParams} onChange={(e) => setRunParams(e.target.value)} rows={3}
                    className="mt-1 w-full border rounded-lg p-1.5 text-xs font-mono" />
                </label>
                <button onClick={runAction} disabled={running}
                  className="w-full rounded-lg bg-stone-900 text-white py-2 text-sm">{running ? "Running…" : "Run action"}</button>
                {runOut && (
                  <pre className="text-[11px] bg-stone-100 rounded-lg p-2 overflow-x-auto max-h-56 overflow-y-auto">
                    {JSON.stringify(runOut, null, 1).slice(0, 3000)}
                  </pre>
                )}
              </div>
            )}
          </aside>
        </div>
      </div>
    </div>
  );
}
