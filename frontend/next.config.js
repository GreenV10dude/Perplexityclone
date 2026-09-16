/** @type {import('next').NextConfig} */
module.exports = {
  reactStrictMode: true,
  // Static export so the site can be hosted on GitHub Pages via Actions.
  // `next dev` is unaffected; `next build` writes frontend/out.
  output: "export",
  trailingSlash: true,
  images: { unoptimized: true },
  // Project pages are served under /<repo>. Set repo variable NEXT_BASE_PATH=/<repo> if needed.
  basePath: process.env.NEXT_BASE_PATH || "",
};
