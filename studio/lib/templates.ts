/** The reel visual templates and music moods, numbered, so a request can say "template 3,
 *  music 6" instead of re-describing a whole look every time. He asked for exactly this:
 *  several finished templates and every music mood in one place before committing an
 *  episode to one. */
export type Template = {
  n: number;
  slug: string;
  name: string;
  thumb: string;
  when: string;
};

export const TEMPLATES: Template[] = [
  {
    n: 1,
    slug: "signature-bug",
    name: "Signature bug (the current classic)",
    thumb: "/templates/a-signature-bug.png",
    when:
      "The default. Dark background, one fixed brand color across every episode, a small corner mark so the series reads as one channel. Use this unless a template below fits the episode better.",
  },
  {
    n: 2,
    slug: "terminal-proof",
    name: "Terminal / proof",
    thumb: "/templates/b-terminal-proof.png",
    when:
      "Technical or agent-heavy content that isn't for a general audience — leans into \"we check everything\" with a gate/pass tag and monospace terminal lines.",
  },
  {
    n: 3,
    slug: "editorial",
    name: "Editorial (matches the website)",
    thumb: "/templates/c-editorial.png",
    when:
      "Simple, calmer content — skills, explainers. Same cream/serif palette as the public site, so a viewer who clicks through from the caption doesn't land somewhere that looks like a different brand.",
  },
  {
    n: 4,
    slug: "before-after",
    name: "Before / after split",
    thumb: "/templates/d-before-after.png",
    when:
      "The episode's whole point is a wrong way vs. a right way — the frame is split in half so both are on screen at once instead of one replacing the other.",
  },
  {
    n: 5,
    slug: "checklist",
    name: "Checklist",
    thumb: "/templates/e-checklist.png",
    when:
      "A how-to with real steps — pairs with the explain-steps skill. Numbered steps stay on screen and light up one at a time as the narration reaches them.",
  },
];

/** Every accent pair an episode has actually shipped with, so the next one doesn't
 *  repeat a color by accident — pulled from each build's own --brass/--ember CSS
 *  variables, not retyped by hand. */
export type UsedAccent = { episode: number; brass: string; ember: string };
export const USED_ACCENTS: UsedAccent[] = [
  { episode: 1, brass: "#FFCF4A", ember: "#FF6B3D" },
  { episode: 2, brass: "#FFCF4A", ember: "#FF6B3D" },
  { episode: 3, brass: "#FFCF4A", ember: "#FF6B3D" },
  { episode: 4, brass: "#FFCF4A", ember: "#FF6B3D" },
  { episode: 5, brass: "#FFCF4A", ember: "#FF6B3D" },
  { episode: 6, brass: "#FFCF4A", ember: "#FF6B3D" },
  { episode: 7, brass: "#FF6B8F", ember: "#FF3D5C" },
  { episode: 8, brass: "#FFCF4A", ember: "#FF6B3D" },
  { episode: 9, brass: "#8FE3FF", ember: "#B98CFF" },
];

export type MusicMood = {
  n: number;
  slug: "neutral" | "urgent" | "bright" | "tense" | "drive";
  name: string;
  when: string;
  /** an actual 8s render of the mood, built with audio/build_music.py, so a mood can be
   *  heard here instead of imagined from a text description */
  sample: string;
};

/** Mirrors audio/build_music.py's MOODS exactly — the real, working options, not a
 *  wishlist. If a mood is added there, add its row here too. */
export const MUSIC_MOODS: MusicMood[] = [
  { n: 1, slug: "neutral", name: "Neutral", sample: "/templates/music/neutral.mp3",
    when: "The default — even, unresolved. Works for most explainer content." },
  { n: 2, slug: "urgent", name: "Urgent", sample: "/templates/music/urgent.mp3",
    when: "Minor, restless, never lands on the root. For exposés and warnings." },
  { n: 3, slug: "bright", name: "Bright", sample: "/templates/music/bright.mp3",
    when: "Major, resolves every four bars. For wins, fixes, things that work." },
  { n: 4, slug: "tense", name: "Tense", sample: "/templates/music/tense.mp3",
    when: "Minor, an 8-chord cycle so it doesn't feel like \"urgent\" transposed. For a slow-build reveal or an escalating warning." },
  { n: 5, slug: "drive", name: "Drive", sample: "/templates/music/drive.mp3",
    when: "Major, forward-moving, a faster harmonic rhythm than \"bright\". For a fix that unfolds in real time rather than one single win." },
];
