"use client";
import { useState } from "react";
import { streamComputer, cancelComputerTask, computerDownloadUrl, API_URL } from "../lib/api";
import { ImageRail } from "./ImageRail";
import { SourceCards } from "./SourceCards";

const AGENT_LABEL = { researcher: "🔍 Researcher", fetcher: "🌐 Fetcher", coder: "💻 Coder", writer: "✍️ Writer" };

export function ComputerView({ settings, connectors }) {
  const [task, setTask] = useState("");
  const [running, setRunning] = useState(false);
  const [taskId, setTaskId] = useState(null);
  const [steps, setSteps] = useState([]);
  const [planner, setPlanner] = useState("");
  const [final, setFinal] = useState("");
  const [sources, setSources] = useState([]);
  const [images, setImages] = useState([]);
  const [files, setFiles] = useState([]);
  const [status, setStatus] = useState("idle");

  async function run() {
    if (!task.trim() || running) return;
    const t = task.trim();
    setTask("");
    setSteps([]); setFinal(""); setSources([]); setImages([]); setFiles([]);
    setStatus("planning"); setRunning(true);
    await streamComputer(
      { task: t, provider: settings.provider, model: settings.model, api_key: settings.api_key, connectors: connectors || [] },
      (e) => {
        if (e.type === "task_started") setTaskId(e.id);
        else if (e.type === "plan") { setSteps(e.steps.map((s) => ({ ...s, status: "pending" }))); setPlanner(e.planner); setStatus("running"); }
        else if (e.type === "step_started") {
          setSteps((s) => s.map((x) => (x.id === e.id ? { ...x, status: "running" } : x)));
        } else if (e.type === "step_done") {
          setSteps((s) => s.map((x) => (x.id === e.id ? { ...e.step } : x)));
          if (e.step.files?.length) setFiles(e.step.files);
        } else if (e.type === "file") {
          setFiles((f) => [...f.filter((x) => x.name !== e.file.name), e.file]);
        } else if (e.type === "done") {
          setStatus(e.status);
          if (e.final) setFinal(e.final);
          if (e.sources) setSources(e.sources);
          if (e.images) setImages(e.images);
          if (e.files) setFiles(e.files);
          setRunning(false);
        }
      }
    );
    setRunning(false);
  }

  async function cancel() {
    if (taskId) await cancelComputerTask(taskId);
  }

  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-stone-200 bg-white p-4">
        <div className="text-sm font-semibold">Perplexity Computer — multi-agent worker</div>
        <div className="text-xs text-stone-500">Planner → parallel researchers → coder sandbox → writer. Runs for minutes, streams progress. {planner && `Planner: ${planner}`}</div>
        <div className="mt-3 flex gap-2">
          <input value={task} onChange={(e) => setTask(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && run()}
            placeholder="Hand off a project: research EV pricing, build a dashboard, analyze a CSV…"
            className="flex-1 rounded-xl border border-stone-300 px-4 py-3 outline-none" />
          {!running
            ? <button onClick={run} className="rounded-xl bg-stone-900 text-white px-5">Run</button>
            : <button onClick={cancel} className="rounded-xl bg-red-700 text-white px-5">Stop</button>}
        </div>
        <div className="mt-2 text-xs text-stone-400">Status: {status} {taskId && `· ${taskId}`}</div>
      </div>

      {steps.length > 0 && (
        <div className="grid gap-3 md:grid-cols-2">
          {steps.map((s) => (
            <div key={s.id} className="rounded-xl border border-stone-200 bg-white p-3">
              <div className="flex items-center gap-2 text-sm font-medium">
                <span>{s.status === "done" ? "✅" : s.status === "running" ? "⏳" : s.status === "error" ? "❌" : "·"}</span>
                <span>{AGENT_LABEL[s.agent] || s.agent}</span>
                <span className="text-stone-400 font-normal">· {s.title}</span>
              </div>
              {s.text && <div className="mt-2 text-xs whitespace-pre-wrap text-stone-700 max-h-48 overflow-y-auto">{s.text.slice(0, 2000)}</div>}
              {s.exec && <div className="mt-1 text-[11px] text-stone-500">exit {s.exec.code}</div>}
            </div>
          ))}
        </div>
      )}

      {(final || sources.length > 0) && (
        <div className="grid gap-6 lg:grid-cols-[1fr_300px]">
          <div className="rounded-2xl border border-stone-200 bg-white p-4">
            <div className="text-xs font-semibold uppercase text-stone-500 mb-2">Deliverable</div>
            <div className="whitespace-pre-wrap text-[15px] leading-7">{final || "Working…"}</div>
            {files.length > 0 && (
              <div className="mt-4">
                <div className="text-xs font-semibold uppercase text-stone-500 mb-2">Files</div>
                {files.map((f) => (
                  <a key={f.name} href={taskId ? computerDownloadUrl(taskId, f.name) : "#"} target="_blank"
                    className="block text-sm underline py-0.5">{f.name} ({f.size}b)</a>
                ))}
              </div>
            )}
          </div>
          <aside className="space-y-4">
            <div>
              <div className="mb-2 text-xs font-semibold uppercase text-stone-500">Images</div>
              <ImageRail images={images} />
            </div>
            <div>
              <div className="mb-2 text-xs font-semibold uppercase text-stone-500">Sources</div>
              <SourceCards sources={sources.map((s, i) => ({ n: i + 1, ...s }))} />
            </div>
          </aside>
        </div>
      )}
    </div>
  );
}
