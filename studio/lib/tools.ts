/** Which real AI tool an episode is about, read straight out of its own title — never a
 *  separate category someone has to remember to set. Order matters: first match wins,
 *  so a title naming two tools still gets one clear tag instead of picking arbitrarily.
 *
 *  Shared between the client-side episode browser and the server-rendered homepage
 *  "browse by tool" row, so the two can never disagree about what an episode's tag is. */
export const TOOLS = ["ChatGPT", "Claude", "Gemini", "n8n", "Instagram", "Whisper", "YouTube", "Agents", "Skills"];

export function toolFor(title: string): string {
  const hit = TOOLS.find((t) => title.toLowerCase().includes(t.toLowerCase()));
  return hit ?? "General";
}
