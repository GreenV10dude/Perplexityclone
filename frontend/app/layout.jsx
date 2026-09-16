export const metadata = { title: "FreePerplexity", description: "Free BYOK Perplexity clone with unlimited SearXNG" };
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head><script src="https://cdn.tailwindcss.com"></script></head>
      <body style={{ margin: 0 }}>{children}</body>
    </html>
  );
}
