"use client";
export function SourceCards({ sources }) {
  if (!sources?.length) return null;
  return (
    <div className="space-y-2">
      {sources.map((s) => (
        <a key={s.n} href={s.url} target="_blank"
          className="block rounded-lg border border-stone-200 p-2.5 hover:bg-stone-50">
          <div className="text-xs text-stone-500">[{s.n}] {s.domain}</div>
          <div className="text-sm font-medium leading-snug">{s.title}</div>
          <div className="text-xs text-stone-600 line-clamp-2">{s.snippet}</div>
        </a>
      ))}
    </div>
  );
}
