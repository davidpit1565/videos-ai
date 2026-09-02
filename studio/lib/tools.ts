/** Which real AI tool an episode is about, read straight out of its own title — never a
 *  separate category someone has to remember to set. Order matters: first match wins,
 *  so a title naming two tools still gets one clear tag instead of picking arbitrarily.
 *
 *  Shared between the client-side episode browser and the server-rendered homepage
 *  "browse by tool" row, so the two can never disagree about what an episode's tag is. */
export const TOOLS = [
  "ChatGPT", "Claude", "Gemini", "n8n", "Instagram", "Whisper", "YouTube", "Agents",
  "Skills", "Comet", "HyperFrames", "Voice",
];

export function toolFor(title: string, extra?: string): string {
  const titleHit = TOOLS.find((t) => title.toLowerCase().includes(t.toLowerCase()));
  if (titleHit) return titleHit;
  if (!extra) return "General";
  // A second pass over the standfirst, for the episodes whose title never names the
  // tool it's actually about — episode 14 ("Everyone's sharing this claim...") tested
  // Claude by name in its own standfirst and still landed in "General" with only the
  // title checked. Two special cases go first, ahead of the general brand scan: an
  // episode about a tool we built (HyperFrames) that happens to also namedrop a
  // compatible AI model in passing must not tag as that model (episode 16 mentions
  // "AI coding agents like Claude" while being fundamentally about HyperFrames itself),
  // and narration/voice-QA episodes aren't about any one brand at all.
  const hay = `${title} ${extra}`.toLowerCase();
  if (hay.includes("hyperframes")) return "HyperFrames";
  if (hay.includes("narration") || hay.includes("voice_doctor") || hay.includes("voice clone")) {
    return "Voice";
  }
  return TOOLS.find((t) => hay.includes(t.toLowerCase())) ?? "General";
}
