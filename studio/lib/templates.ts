/** The reel visual templates and music moods, numbered, so a request can say "template 3,
 *  music 6" instead of re-describing a whole look every time. He asked for exactly this:
 *  several finished templates and every music mood in one place before committing an
 *  episode to one. */
import usedDesigns from "../../channel/used-designs.json";

export type Template = {
  n: number;
  slug: string;
  name: string;
  thumb: string;
  when: string;
  /** the specific psychological principle the template leans on, when it's built around
   *  one — named plainly so it can be checked against real research, not invoked as a
   *  vague "this feels more engaging" */
  psychology?: string;
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
  {
    n: 6,
    slug: "curiosity-gap",
    name: "Curiosity gap",
    thumb: "/templates/f-curiosity-gap.png",
    when:
      "The hook names a specific fix but blanks out the actual word — the redacted part is what makes someone stay for the reveal, not the sentence around it.",
    psychology:
      "Zeigarnik effect: an unfinished thing occupies attention longer than a finished one. Use the redaction on the one word that actually resolves the episode — a vague blank with nothing real behind it reads as clickbait the moment it's revealed.",
  },
  {
    n: 7,
    slug: "loss-framing",
    name: "Loss framing",
    thumb: "/templates/g-loss-framing.png",
    when:
      "The episode's fix prevents an ongoing cost — hours, a bad send, a wrong answer that shipped. Leads with what NOT fixing it is already costing, not with what fixing it gains.",
    psychology:
      "Loss aversion (Kahneman & Tversky): a framed loss moves people more than an equivalent framed gain. Only honest when the number is real or clearly a representative estimate — never invent a specific figure for a hypothetical.",
  },
  {
    n: 8,
    slug: "social-proof",
    name: "Social proof",
    thumb: "/templates/h-social-proof.png",
    when:
      "There's a real, measured number behind the claim — setups tested, checks run, episodes shipped. The number IS the hook, not a decoration next to it.",
    psychology:
      "Cialdini's social proof: people trust what a number of others have already done more than an unsupported claim. Per CLAUDE.md's own rule — never a placeholder or rounded-up number, the exact measured one or nothing.",
  },
  {
    n: 9,
    slug: "pattern-interrupt",
    name: "Pattern interrupt",
    thumb: "/templates/i-pattern-interrupt.png",
    when:
      "The first 0.5s only — a glitch/scramble burst that resolves into the real headline. For a topic that needs to stop a scrolling thumb before it explains anything.",
    psychology:
      "Pattern interrupt: a break in visual rhythm resets the brain's habitual scroll-past response for a beat. Keep it to the opening beat only — sustained through the video it reads as broken rather than deliberate.",
  },
  {
    n: 10,
    slug: "receipts",
    name: "Receipts",
    thumb: "/templates/j-receipts.png",
    when:
      "The proof is inherently a log or a check output — check.sh, a terminal run, a before/after diff. Shows the actual evidence instead of a claim about it.",
    psychology:
      "Authority/evidence bias: a raw log reads as proof in a way an assertion never does, because it looks like something that wasn't written to persuade. Only ever show real output — a fabricated terminal line is the one thing this channel can't survive being caught doing.",
  },
];

/** Every accent pair (and music mood) an episode has actually shipped with, read from
 *  the same file export/produce.sh writes to and checks against before shipping a new
 *  one — a real enforcement now, not a table someone has to remember to consult. This
 *  used to be a hardcoded array here that nothing kept in sync with the actual builds;
 *  moved to channel/used-designs.json so there's exactly one source of truth for both
 *  the shell pipeline and this page. `mood` is null for episodes shipped before
 *  produce.sh tracked it — not a guessed "neutral", an honest gap. */
export type UsedAccent = { episode: number; brass: string; ember: string; mood: string | null };
export const USED_ACCENTS: UsedAccent[] = usedDesigns;

export type MusicMood = {
  n: number;
  slug: string;
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
  { n: 6, slug: "sparse", name: "Sparse", sample: "/templates/music/sparse.mp3",
    when: "Almost nothing playing — sub bass and a slow chime, no arp, no percussion. A minimalist reveal or a single-fact explainer with nothing fighting for attention under it." },
  { n: 7, slug: "playful", name: "Playful", sample: "/templates/music/playful.mp3",
    when: "Short plucky notes instead of a held pad, bouncy and major. Lighthearted or beginner-friendly content." },
  { n: 8, slug: "corporate", name: "Corporate", sample: "/templates/music/corporate.mp3",
    when: "Clean, steady, no arpeggio, barely-there percussion. Confident rather than moody — for \"sell this to a business\" content." },
  { n: 9, slug: "glitch", name: "Glitch", sample: "/templates/music/glitch.mp3",
    when: "Irregular and dissonant, a mechanical stutter under it. For an agent-failure cold open only — never a whole episode." },
  { n: 10, slug: "cinematic", name: "Cinematic", sample: "/templates/music/cinematic.mp3",
    when: "One chord per two bars, a huge slow pad swell, no percussion at all. A big reveal or a stakes-setting cold open." },
  { n: 11, slug: "lofi", name: "Lo-fi", sample: "/templates/music/lofi.mp3",
    when: "Warm, filtered, a slow swung arp. A wind-down or a calmer explainer that doesn't need \"neutral\"'s full room." },
  { n: 12, slug: "retro", name: "Retro", sample: "/templates/music/retro.mp3",
    when: "Fast triangle-wave sixteenth arpeggio, bright, almost no pad swell. A \"remember when\" or tools-through-time bit." },
  { n: 13, slug: "suspense", name: "Suspense", sample: "/templates/music/suspense.mp3",
    when: "Sparse minor-second dissonance with a fast tremolo swell — slow-build dread rather than \"tense\"'s escalating warning. Use sparingly." },
  { n: 14, slug: "triumphant", name: "Triumphant", sample: "/templates/music/triumphant.mp3",
    when: "Full pad, arp, and a kick on every beat instead of two — the only mood that resolves and hits hard at once. A genuine \"it works, and here's the proof\" close." },
  { n: 15, slug: "clockwork", name: "Clockwork", sample: "/templates/music/clockwork.mp3",
    when: "A steady mechanical sixteenth-note pulse with no swell and no rubato. Automation/workflow content where the point is that the machine doesn't waver." },
  { n: 16, slug: "piano", name: "Piano", sample: "/templates/music/piano.mp3",
    when: "Plucked-string synthesis (Karplus-Strong, not a sample), struck once per bar and left to decay rather than held. Bright, fast decay. A calm walkthrough or skills explainer that wants warmth without a full pad bed." },
  { n: 17, slug: "guitar", name: "Guitar", sample: "/templates/music/guitar.mp3",
    when: "Same synthesis as Piano, tuned warmer and longer-ringing — a chord rings into the next instead of striking and dying. A personal or behind-the-scenes bit, or anything that wants an organic rather than digital feel." },
];

export type Avatar = {
  n: number;
  slug: string;
  name: string;
  thumb: string;
  when: string;
};

/** The D-ID avatar wardrobe — one consistent generated face (kept anchored across
 *  separate ChatGPT image-edit passes, never regenerated from scratch) in 32 scenes, each
 *  one built for a specific episode topic. "Avatar 9" instead of re-describing "the one
 *  with the double shadow, for the retry episode" every time. Full detail in
 *  studio/public/avatars/MANIFEST.md. */
export const AVATARS: Avatar[] = [

  { n: 1, slug: "amber-default", name: "Amber default", thumb: "/avatars/avatar-01-amber-default.png",
    when: "The default — most episodes." },
  { n: 2, slug: "tech-casual", name: "Tech casual", thumb: "/avatars/avatar-02-tech-casual.png",
    when: "Everyday/casual episodes." },
  { n: 3, slug: "collared-neutral", name: "Collared neutral", thumb: "/avatars/avatar-03-collared-neutral.png",
    when: "Slightly more formal than tech-casual, still everyday." },
  { n: 4, slug: "cool-blue", name: "Cool blue", thumb: "/avatars/avatar-04-cool-blue.png",
    when: "Bug/failure episodes." },
  { n: 5, slug: "warm-bright", name: "Warm bright", thumb: "/avatars/avatar-05-warm-bright.png",
    when: "Success/solution episodes." },
  { n: 6, slug: "wet-watermarks", name: "Wet", thumb: "/avatars/avatar-06-wet-watermarks.png",
    when: "Watermark-related topics — a literal visual pun." },
  { n: 7, slug: "particles-agents", name: "Particles", thumb: "/avatars/avatar-07-particles-agents.png",
    when: "AI agents / agentic workflows." },
  { n: 8, slug: "glass-transparency", name: "Glass panel", thumb: "/avatars/avatar-08-glass-transparency.png",
    when: "Audit / transparency / verification topics." },
  { n: 9, slug: "double-shadow-retry", name: "Double shadow", thumb: "/avatars/avatar-09-double-shadow-retry.png",
    when: "Retry/duplicate/idempotency topics — episode 25's own subject." },
  { n: 10, slug: "chain-workflow", name: "Glowing chain", thumb: "/avatars/avatar-10-chain-workflow.png",
    when: "Automation / n8n / workflow-chaining topics." },
  { n: 11, slug: "disintegration-ai-reveal", name: "Disintegration", thumb: "/avatars/avatar-11-disintegration-ai-reveal.png",
    when: " \"This is AI\" reveal moments." },
  { n: 12, slug: "gears-efficiency", name: "Blurred gears", thumb: "/avatars/avatar-12-gears-efficiency.png",
    when: "Speed / efficiency topics." },
  { n: 13, slug: "bright-eyes-reflection", name: "Bright eyes", thumb: "/avatars/avatar-13-bright-eyes-reflection.png",
    when: "Code / technical-tool topics." },
  { n: 14, slug: "red-urgent", name: "Red urgent", thumb: "/avatars/avatar-14-red-urgent.png",
    when: "Urgent/warning episodes." },
  { n: 15, slug: "gold-triumphant", name: "Gold triumphant", thumb: "/avatars/avatar-15-gold-triumphant.png",
    when: "Confident wins." },
  { n: 16, slug: "suspense-dark", name: "Suspense dark", thumb: "/avatars/avatar-16-suspense-dark.png",
    when: "Slow-build reveal / suspense cold opens." },
  { n: 17, slug: "corporate-suit", name: "Corporate suit", thumb: "/avatars/avatar-17-corporate-suit.png",
    when: "Business/selling-to-clients topics." },
  { n: 18, slug: "tech-jacket", name: "Tech jacket", thumb: "/avatars/avatar-18-tech-jacket.png",
    when: "Modern technical topics, between casual and formal." },
  { n: 19, slug: "plain-tshirt", name: "Plain t-shirt", thumb: "/avatars/avatar-19-plain-tshirt.png",
    when: "Most casual/accessible episodes." },
  { n: 20, slug: "1920s-suit", name: "1920s suit", thumb: "/avatars/avatar-20-1920s-suit.png",
    when: "\"Principles/fundamentals\" episodes." },
  { n: 21, slug: "coins-cost", name: "Coins bokeh", thumb: "/avatars/avatar-21-coins-cost.png",
    when: "Pricing / cost-savings topics." },
  { n: 22, slug: "lock-security", name: "Glowing lock", thumb: "/avatars/avatar-22-lock-security.png",
    when: "Security / privacy topics." },
  { n: 23, slug: "motion-blur-speed", name: "Motion blur", thumb: "/avatars/avatar-23-motion-blur-speed.png",
    when: "Speed / automation topics." },
  { n: 24, slug: "split-comparison", name: "Split lighting", thumb: "/avatars/avatar-24-split-comparison.png",
    when: "A-vs-B / this-vs-that comparison topics." },
  { n: 25, slug: "circuit-api", name: "Circuit lines", thumb: "/avatars/avatar-25-circuit-api.png",
    when: "API / integration topics." },
  { n: 26, slug: "soundwave-audio", name: "Soundwave", thumb: "/avatars/avatar-26-soundwave-audio.png",
    when: "Voice / audio topics." },
  { n: 27, slug: "second-face-teamwork", name: "Second face", thumb: "/avatars/avatar-27-second-face-teamwork.png",
    when: "Multi-agent / teamwork topics." },
  { n: 28, slug: "grid-data", name: "Data grid", thumb: "/avatars/avatar-28-grid-data.png",
    when: "Data / analytics topics." },
  { n: 29, slug: "city-bokeh-mobile", name: "City bokeh", thumb: "/avatars/avatar-29-city-bokeh-mobile.png",
    when: "Mobile / on-the-go topics." },
  { n: 30, slug: "crack-warning", name: "Crack line", thumb: "/avatars/avatar-30-crack-warning.png",
    when: "Mistake / warning episodes." },
  { n: 31, slug: "magnifier-search", name: "Magnifier", thumb: "/avatars/avatar-31-magnifier-search.png",
    when: "Search / discovery topics." },
  { n: 32, slug: "sparkle-milestone", name: "Sparkle", thumb: "/avatars/avatar-32-sparkle-milestone.png",
    when: "Milestone / anniversary episodes." },
];
