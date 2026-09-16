"use client";
import { useState } from "react";
import { proxiedImage, API_URL } from "../lib/api";

export function ImageRail({ images }) {
  const [lightbox, setLightbox] = useState(null);
  if (!images?.length)
    return (
      <div className="grid grid-cols-3 gap-2">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="aspect-square rounded-lg bg-stone-200 animate-pulse" />
        ))}
      </div>
    );
  return (
    <>
      <div className="grid grid-cols-3 gap-2">
        {images.map((im, i) => (
          <button key={i} onClick={() => setLightbox(im)}
            className="group relative aspect-square overflow-hidden rounded-lg bg-stone-100 border border-stone-200"
            title={im.title}>
            <img src={proxiedImage(API_URL, im.thumb)} alt={im.title || "result"}
              loading="lazy"
              className="h-full w-full object-cover group-hover:scale-105 transition"
              onError={(e) => { e.target.style.display = "none"; }} />
          </button>
        ))}
      </div>
      {lightbox && (
        <div className="fixed inset-0 z-50 bg-black/70 flex items-center justify-center p-6" onClick={() => setLightbox(null)}>
          <div className="bg-white rounded-xl max-w-2xl w-full overflow-hidden" onClick={(e) => e.stopPropagation()}>
            <img src={proxiedImage(API_URL, lightbox.full)} alt={lightbox.title} className="w-full max-h-[70vh] object-contain bg-black" />
            <div className="p-4 flex items-center justify-between">
              <div className="text-sm truncate">{lightbox.title} · {lightbox.source}</div>
              <a href={lightbox.source_url} target="_blank" className="text-sm underline">Visit source</a>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
