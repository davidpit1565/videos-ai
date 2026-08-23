import { PROMPTS } from "./prompts";

/** The written half of an episode.
 *
 *  The caption cannot carry this — Instagram allows 2200 characters and the prompt alone
 *  is 1169, so the explanation had nowhere to live except a page. It lives here rather
 *  than in the database because it is content, it belongs in review, and an episode page
 *  should not be empty just because nobody has typed notes into the studio yet.
 *
 *  The studio still wins where it knows more: a live episode supplies the title, the
 *  YouTube id and its own notes, and those are merged on top of this. */
export type Article = {
  n: number;
  title: string;
  standfirst: string;
  /** the exact clicks, because that is the channel's whole promise */
  steps: string[];
  changes: string[];
  /** what it will not do. Never optional. */
  limits: string[];
  promptSlug?: string;
};

export const ARTICLES: Article[] = [
  {
    n: 1,
    title: "One paste, and ChatGPT stops giving you the obvious",
    standfirst:
      "Most answers are generic because nothing ever told the model how to think. " +
      "This is one block of text you paste once. After that it picks its own method for " +
      "every question — no commands, no shortcuts, nothing to remember.",
    steps: [
      "Open ChatGPT and go to Settings.",
      "Open Personalization.",
      "Open Custom instructions.",
      "Paste the prompt below into the box.",
      "Switch it on, and press Save.",
    ],
    changes: [
      "It states what it is assuming, instead of guessing silently.",
      "It names the risk you did not ask about.",
      "It ends with a decision rather than a list of options.",
      "You type zero commands. Same model, different method.",
    ],
    limits: [
      "It cannot browse the web and it cannot read your files — it changes how the model reasons, not what it can reach.",
      "On a brand-new chat the first answer is sometimes still generic. Ask once more and it settles.",
      "It is not a jailbreak and it does not raise any usage limit.",
      "Custom instructions are per-account, not per-device: it follows you, and it also applies to chats you would rather it left alone.",
    ],
    promptSlug: "universal-ai-engine",
  },
  {
    n: 2,
    title: "What an AI agent actually is",
    standfirst:
      "Everyone says agent. Almost nobody can tell you where the chatbot ends. " +
      "It is three steps on a loop, and one test settles it in a sentence.",
    // No prompt to paste in this one, so the steps ARE the test. The channel's promise is
    // the exact thing to do, and here the exact thing to do is apply the test to whatever
    // tool the viewer is already paying for.
    steps: [
      "Take whatever you are calling an agent — a GPT, a chatbot, an automation.",
      "Give it a job with more than one step, and do not tell it the steps.",
      "Watch whether it plans the steps itself, or waits for you to name each one.",
      "Check whether it used a real tool — sent, wrote, fetched, booked — or only described one.",
      "Check whether it looked at what came back before continuing.",
    ],
    changes: [
      "Plan, act, check, on a loop. That loop is the entire difference.",
      "A chatbot answers. An agent acts — it decides the steps itself.",
      "Acting means a tool that touches something real, not a description of the tool.",
      "If it cannot act without you, it is a chatbot with a better name.",
    ],
    limits: [
      "Agents do not fail like chatbots. A chatbot gives you a bad answer; an agent fails confidently, halfway through, having already done part of the work.",
      "That is why the first one you build should touch something reversible — a draft, not a send.",
      "Nothing here makes an agent reliable. It makes the word mean something, which is what the rest depends on.",
      "The loop is the definition, not a product. Two tools can both have it and one can still be useless for your job.",
    ],
  },
  {
    n: 3,
    title: "Your AI agent is already lying to you",
    standfirst:
      "Five ways agents fail silently, in every real build — not a hype reel, the honest list. " +
      "One line to add to your own prompt closes the worst of them.",
    steps: [
      "Open the system prompt of any agent you have built or are testing.",
      "Add one sentence: \"If you're not sure, say so instead of guessing.\"",
      "Give it a task where the honest answer is \"I don't know\" or \"this failed.\"",
      "Check what it actually says — not what it does next, what it reports.",
      "If it still claims success on a failure, the prompt line did not fix the underlying problem, only the wording.",
    ],
    changes: [
      "It says it's done when it is not — check the actual result, not the report.",
      "It guesses instead of saying \"I don't know,\" unless told explicitly that guessing is worse.",
      "It forgets everything from the previous run unless you build memory in yourself.",
      "It breaks on a login screen or CAPTCHA, every time, with no graceful fallback.",
      "Once it sends something, there is no undo — which is why the first thing it touches should be reversible.",
    ],
    limits: [
      "One prompt line does not make an agent reliable. It changes what it reports, not what it can actually do.",
      "Nothing here is unique to one platform — this is what the failure modes look like across every agent we've tested.",
    ],
  },
  {
    n: 4,
    title: "This video almost shipped broken",
    standfirst:
      "Three real defects reached us before a person caught them, on our own pipeline. " +
      "None was caught by a tool. That's why every check here now checks the check before it.",
    steps: [
      "Before trusting any automated check, feed it a case you already know is broken.",
      "Confirm the check actually flags that known-bad case — not just that it runs without error.",
      "Only then trust it on real, unknown cases.",
      "Re-run this test after any change to the check itself, not just after changes to what it checks.",
    ],
    changes: [
      "A level check measured the wrong thing — it read a position in the file, not whether the sound had actually landed.",
      "A check ran before the fix it was supposed to verify, so it always passed.",
      "A script proved a file existed by checking its path, not its contents — the file was empty.",
      "None of these three were caught by a tool. A person listening, reading, and checking by hand caught all three.",
    ],
    limits: [
      "Testing a check against a known-bad case does not guarantee it catches every bad case — only the ones like the one you tested.",
      "This is a discipline, not a one-time fix. The three defects here happened after checks already existed; the checks just weren't checked.",
    ],
  },
  {
    n: 5,
    title: "Your captions are hiding behind Instagram",
    standfirst:
      "Meta publishes the numbers: the bottom third of a 9:16 frame is where the interface " +
      "draws its own UI. We measured our own videos and found the same mistake.",
    steps: [
      "Open any 1080×1920 video you've made for Reels, Shorts, or TikTok.",
      "Check where your captions and key text actually sit on screen.",
      "Keep everything inside: top 269px and bottom 672px are off-limits on 1080×1920.",
      "Re-check after any edit — a caption that grows by one line can drift back into the unsafe zone.",
    ],
    changes: [
      "80.2% of short clips carry captions and 78.6% animate them — captions are not optional in this format.",
      "A caption sitting in the bottom third is technically rendered but sits behind the platform's own username, audio label, and buttons.",
      "The safe box on 1080×1920 is x 65-1015, y 269-1248 — everything meant to be read belongs inside it.",
    ],
    limits: [
      "This is Instagram and TikTok's current UI. Platforms change their layouts, and the exact numbers can shift.",
      "Decorative background elements can still use the full frame — only text and anything meant to be read needs to respect the safe box.",
    ],
  },
  {
    n: 6,
    title: "One word broke our pipeline 20 times",
    standfirst:
      "A quality check kept flagging the word \"three\" as broken. Twice, it was right and pointed " +
      "at a real bug. After that, it kept failing anyway — for a reason no tool could tell us.",
    steps: [
      "When an automated check keeps failing on the same case, don't silence it — investigate first.",
      "Fix every real bug the check surfaces, verifying each fix on real generated output.",
      "If it still fails after real fixes are confirmed, run it and listen or look yourself.",
      "If your own judgment overrides the metric, write down why, in the same place the check's output lives.",
    ],
    changes: [
      "Two real bugs were found this way: a stretch guard that never actually ran, and a silence-trim that cut off the start of the word.",
      "After both fixes, the same word still failed the check roughly 20 more times, across two different sentences.",
      "The conclusion, confirmed by listening: this specific voice model cannot reliably land that consonant at the very start of a sentence.",
      "The gate now has an explicit override — a human's approval by ear, recorded in the file, not a silently disabled check.",
    ],
    limits: [
      "An override is not a fix. The underlying limitation is still there; it is now documented instead of hidden.",
      "This does not mean every repeated failure is the tool's fault — most of the time it still means real work to do. This was confirmed, not assumed.",
    ],
  },
];

export const articleFor = (n: number) => ARTICLES.find((a) => a.n === n) ?? null;
export const promptFor = (a: Article | null) =>
  a?.promptSlug ? PROMPTS.find((p) => p.slug === a.promptSlug) ?? null : null;
