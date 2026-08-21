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
];

export const articleFor = (n: number) => ARTICLES.find((a) => a.n === n) ?? null;
export const promptFor = (a: Article | null) =>
  a?.promptSlug ? PROMPTS.find((p) => p.slug === a.promptSlug) ?? null : null;
