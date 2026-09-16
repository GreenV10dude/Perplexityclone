"use client";
import { useEffect, useState } from "react";
import { fetchModels } from "../lib/api";

export function SettingsModal({ open, onClose, settings, setSettings }) {
  const [providers, setProviders] = useState([]);
  useEffect(() => {
    if (open) fetchModels().then((d) => setProviders(d.providers || [])).catch(() => {});
  }, [open ]);
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-white rounded-2xl w-full max-w-lg p-6 space-y-4" onClick={(e) => e.stopPropagation()}>
        <h2 className="text-lg font-semibold">Bring your own key — free forever, unlimited search</h2>
        <label className="block text-sm">Provider
          <select value={settings.provider} onChange={(e) => setSettings({ ...settings, provider: e.target.value })}
            className="mt-1 w-full border rounded-lg p-2">
            {providers.map((p) => <option key={p.id} value={p.id}>{p.label}</option>)}
          </select>
        </label>
        <label className="block text-sm">Model
          <input value={settings.model} onChange={(e) => setSettings({ ...settings, model: e.target.value })}
            className="mt-1 w-full border rounded-lg p-2" placeholder="gpt-4o-mini / claude-sonnet-4-5 / gemini-2.5-flash" />
        </label>
        <label className="block text-sm">API key (stored locally only)
          <input type="password" value={settings.api_key} onChange={(e) => setSettings({ ...settings, api_key: e.target.value })}
            className="mt-1 w-full border rounded-lg p-2" placeholder="sk-..." />
        </label>
        <p className="text-xs text-stone-500">
          Search via bundled SearXNG is unlimited with no key. LLM synthesis uses your key via LiteLLM —
          supports OpenAI, Anthropic, Gemini, xAI, DeepSeek, Mistral, Groq, Together, OpenRouter, HF, Ollama + 10 more.
        </p>
        <button onClick={onClose} className="w-full rounded-lg bg-stone-900 text-white py-2">Done</button>
      </div>
    </div>
  );
}
