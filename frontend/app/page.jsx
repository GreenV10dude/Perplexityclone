"use client";
import { useEffect, useState } from "react";
import { streamChat } from "../lib/api";
import { AnswerView } from "../components/AnswerView";
import { SettingsModal } from "../components/SettingsModal";
import { ComputerView } from "../components/ComputerView";
import { ConnectorsPanel } from "../components/ConnectorsPanel";

const MODES = ["Search", "Research", "Reason", "Create", "Computer"];

export default function Home() {
  const [query, setQuery] = useState("");
  const [mode, setMode] = useState("Search");
  const [turns, setTurns] = useState([]);
  const [loading, setLoading] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [connectorsOpen, setConnectorsOpen] = useState(false);
  const [activeConnectors, setActiveConnectors] = useState([]);
  const [connectorCreds, setConnectorCreds] = useState({});
  const [settings, setSettings] = useState({ provider: "openai", model: "gpt-4o-mini", api_key: "" });

  useEffect(() => {
    try {
      const saved = JSON.parse(localStorage.getItem("fpx_connectors") || "{}");
      if (saved.active) setActiveConnectors(saved.active);
      if (saved.creds) setConnectorCreds(saved.creds);
    } catch {}
  }, []);
  useEffect(() => {
    try {
      localStorage.setItem("fpx_connectors", JSON.stringify({ active: activeConnectors, creds: connectorCreds }));
    } catch {}
  }, [activeConnectors, connectorCreds]);

  async function ask() {
    if (!query.trim() || loading) return;
    const q = query.trim();
    setQuery("");
    const idx = turns.length;
    setTurns((t) => [...t, { query: q, text: "", images: [], sources: [], instance: "" }]);
    setLoading(true);
    await streamChat(
      { query: q, provider: settings.provider, model: settings.model, api_key: settings.api_key, deep: mode === "Research", connectors: activeConnectors },
      (e) => {
        if (e.type === "meta") {
          setTurns((t) => t.map((x, i) => (i === idx ? { ...x, images: e.images, sources: e.sources, instance: e.instance } : x)));
        } else if (e.type === "token") {
          setTurns((t) => t.map((x, i) => (i === idx ? { ...x, text: x.text + e.text } : x)));
        }
      }
    );
    setLoading(false);
  }

  return (
    <div className="flex h-screen bg-[#f7f5f0] text-stone-900">
      {/* Claude-like sidebar */}
      <aside className="w-64 shrink-0 border-r border-stone-200 bg-[#efece5] p-4 hidden md:flex flex-col gap-3">
        <button onClick={() => setTurns([])} className="rounded-lg bg-stone-900 text-white py-2 text-sm">+ New chat</button>
        <div className="text-xs font-semibold uppercase text-stone-500 mt-2">Modes</div>
        {MODES.map((m) => (
          <button key={m} onClick={() => setMode(m)}
            className={`text-left text-sm rounded-lg px-3 py-1.5 ${mode === m ? "bg-white shadow" : "hover:bg-white/60"}`}>{m}</button>
        ))}
        <div className="text-xs font-semibold uppercase text-stone-500 mt-2">Workspace</div>
        {["Projects", "Library"].map((x) => (
          <div key={x} className="text-sm px-3 py-1.5 text-stone-600">{x}</div>
        ))}
        <button onClick={() => setConnectorsOpen(true)}
          className="text-left text-sm rounded-lg px-3 py-1.5 hover:bg-white/60">
          🔌 Connectors{activeConnectors.length ? ` (${activeConnectors.length})` : ""}
        </button>
        <div className="mt-auto">
          <button onClick={() => setSettingsOpen(true)} className="w-full text-sm rounded-lg border py-2 bg-white">
            ⚙ {settings.provider} · BYOK {settings.api_key ? "✓" : "—"}
          </button>
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 flex flex-col min-w-0">
        <header className="border-b border-stone-200 px-6 py-3 flex items-center gap-2 text-sm">
          <span className="font-semibold">FreePerplexity</span>
          <span className="text-stone-400">· {mode} · images always on · unlimited SearXNG</span>
          <button onClick={() => setSettingsOpen(true)} className="ml-auto md:hidden border rounded-lg px-3 py-1">Settings</button>
        </header>
        <div className="flex-1 overflow-y-auto px-6 py-6 space-y-10 max-w-6xl w-full mx-auto">
          {mode === "Computer" ? (
            <ComputerView settings={settings} connectors={activeConnectors} />
          ) : (
            <>
              {turns.length === 0 && (
                <div className="text-center mt-20">
                  <h1 className="text-3xl">Where curiosity meets free search</h1>
                  <p className="text-stone-500 mt-2">Ask anything — web + images load every time, thumbnails on the side.</p>
                </div>
              )}
              {turns.map((t, i) => <AnswerView key={i} turn={t} />)}
            </>
          )}
        </div>
        <div className="border-t border-stone-200 p-4">
          <div className="max-w-3xl mx-auto">
            <div className="flex gap-2 mb-2 flex-wrap">
              {MODES.map((m) => (
                <button key={m} onClick={() => setMode(m)}
                  className={`text-xs rounded-full px-3 py-1 border ${mode === m ? "bg-stone-900 text-white" : "bg-white"}`}>{m}</button>
              ))}
            </div>
            <div className="flex gap-2">
              <input value={query} onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && ask()}
                placeholder="Ask anything…"
                className="flex-1 rounded-xl border border-stone-300 bg-white px-4 py-3 outline-none" />
              <button onClick={ask} disabled={loading}
                className="rounded-xl bg-stone-900 text-white px-5">{loading ? "…" : "→"}</button>
            </div>
          </div>
        </div>
      </main>
      <SettingsModal open={settingsOpen} onClose={() => setSettingsOpen(false)} settings={settings} setSettings={setSettings} />
      <ConnectorsPanel open={connectorsOpen} onClose={() => setConnectorsOpen(false)}
        active={activeConnectors} setActive={setActiveConnectors} creds={connectorCreds} setCreds={setConnectorCreds} />
    </div>
  );
}
