/** @type {import('next').NextConfig} */
export default {
  reactStrictMode: true,
  // Never pack the reels or the channel folder into a serverless function. Nothing reads
  // them at request time any more (lib/reels-manifest.json holds the facts), and doing so
  // is what pushed Vercel's Functions Storage to 162 GB (6.10.2026).
  outputFileTracingExcludes: { "*": ["public/reels/**", "../channel/**"] },
};
