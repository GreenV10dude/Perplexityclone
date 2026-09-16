"use client";
import { ImageRail } from "./ImageRail";
import { SourceCards } from "./SourceCards";

export function AnswerView({ turn }) {
  return (
    <div className="w-full">
      {/* Prompt on top */}
      <div className="text-lg font-semibold text-stone-900">{turn.query}</div>
      {/* Text directly below prompt (left) + thumbnails rail (right) */}
      <div className="mt-3 grid gap-6 lg:grid-cols-[1fr_300px]">
        <div className="min-w-0">
          <div className="whitespace-pre-wrap text-[15px] leading-7 text-stone-800">
            {turn.text || <span className="text-stone-400">Searching…</span>}
          </div>
          {turn.instance && (
            <div className="mt-3 text-[11px] text-stone-400">via {turn.instance} · unlimited SearXNG</div>
          )}
        </div>
        <aside className="lg:sticky lg:top-4 h-fit space-y-4">
          <div>
            <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-stone-500">Images</div>
            <ImageRail images={turn.images} />
          </div>
          <div>
            <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-stone-500">Sources</div>
            <SourceCards sources={turn.sources} />
          </div>
        </aside>
      </div>
    </div>
  );
}
