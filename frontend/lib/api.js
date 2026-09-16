export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const PROVIDERS_FALLBACK = [
  "openai", "anthropic", "gemini", "xai", "deepseek", "mistral", "cohere",
  "groq", "together", "fireworks", "openrouter", "huggingface", "qwen",
  "zhipu", "moonshot", "nvidia", "azure", "bedrock", "vertex", "ollama",
].map((id) => ({ id, label: id }));

function demoImages(q) {
  const seed = encodeURIComponent(q || "demo");
  return [1, 2, 3, 4, 5, 6].map((i) => ({
    thumb: `https://picsum.photos/seed/${seed}-${i}/300`,
    full: `https://picsum.photos/seed/${seed}-${i}/1200`,
    title: `Demo image ${i} for ${q}`,
    source: "picsum.photos",
    source_url: "https://picsum.photos",
  }));
}

function demoSources(q) {
  return [1, 2, 3].map((i) => ({
    n: i,
    title: `Demo source ${i} for "${q}" (connect backend for live SearXNG)`,
    url: "https://example.com",
    snippet: "Static demo mode — deploy the FastAPI backend or run it locally for unlimited live search.",
    domain: "example.com",
    engine: "demo",
  }));
}

export async function fetchModels() {
  try {
    const r = await fetch(`${API_URL}/api/models`);
    if (!r.ok) throw new Error("offline");
    return r.json();
  } catch {
    return { providers: PROVIDERS_FALLBACK, demo: true };
  }
}

export async function fetchConnectors() {
  const r = await fetch(`${API_URL}/api/connectors`);
  if (!r.ok) throw new Error("offline");
  return r.json();
}

export async function executeConnector(body) {
  try {
    const r = await fetch(`${API_URL}/api/connectors/execute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    return r.json();
  } catch {
    return { ok: true, demo: true, connector: body.connector_id, action: body.action,
             warning: "Backend offline — static demo result.", result: { items: [], count: 0 } };
  }
}

async function readSSE(res, onEvent) {
  const reader = res.body.getReader();
  const dec = new TextDecoder();
  let buf = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += dec.decode(value, { stream: true });
    const parts = buf.split("\n\n");
    buf = parts.pop() || "";
    for (const p of parts) {
      const line = p.trim();
      if (line.startsWith("data:")) {
        try { onEvent(JSON.parse(line.slice(5).trim())); } catch (e) {}
      }
    }
  }
}

export async function streamChat(body, onEvent) {
  try {
    const r = await fetch(`${API_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!r.ok || !r.body) throw new Error("offline");
    await readSSE(r, onEvent);
  } catch {
    // Static-hosting demo: site stays usable without the backend.
    onEvent({ type: "meta", images: demoImages(body.query), sources: demoSources(body.query), instance: "demo (backend offline)" });
    const apps = (body.connectors || []).join(", ");
    onEvent({ type: "token", text: `Demo answer for: ${body.query}\n\nThis static build has no backend attached, so this is sample output. ` +
      `Run the FastAPI backend (see README) for unlimited SearXNG search + your BYOK key.\n` +
      (apps ? `\nLinked apps passed with this query: ${apps}.\n` : "") });
    onEvent({ type: "done" });
  }
}

export function proxiedImage(apiUrl, url) {
  return `${apiUrl}/api/image?url=${encodeURIComponent(url)}`;
}

export async function streamComputer(body, onEvent) {
  try {
    const r = await fetch(`${API_URL}/api/computer/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!r.ok || !r.body) throw new Error("offline");
    await readSSE(r, onEvent);
  } catch {
    const steps = [
      { id: "s1", agent: "researcher", title: "Web research", status: "pending", text: "" },
      { id: "s2", agent: "coder", title: "Build / compute in sandbox", status: "pending", text: "" },
      { id: "s3", agent: "writer", title: "Final deliverable", status: "pending", text: "" },
    ];
    onEvent({ type: "task_started", id: "demo" });
    onEvent({ type: "plan", steps, planner: "demo (backend offline)" });
    for (const s of steps) {
      onEvent({ type: "step_started", id: s.id, step: s });
      onEvent({ type: "step_done", id: s.id,
                step: { ...s, status: "done", text: `Demo output for ${s.title} — connect the backend for the live multi-agent run.` } });
    }
    onEvent({ type: "done", status: "done",
              final: `Demo deliverable for: ${body.task}\n\nConnect the FastAPI backend for the live planner → researcher → coder → writer run.`,
              sources: demoSources(body.task), images: demoImages(body.task), files: [] });
  }
}

export async function listComputerTasks() {
  try {
    const r = await fetch(`${API_URL}/api/computer/tasks`);
    return r.json();
  } catch {
    return { tasks: [] };
  }
}

export async function cancelComputerTask(id) {
  const r = await fetch(`${API_URL}/api/computer/tasks/${id}/cancel`, { method: "POST" });
  return r.json();
}

export function computerDownloadUrl(id, name) {
  return `${API_URL}/api/computer/tasks/${id}/download?name=${encodeURIComponent(name)}`;
}
