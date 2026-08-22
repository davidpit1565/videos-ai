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
];

export const articleFor = (n: number) => ARTICLES.find((a) => a.n === n) ?? null;
export const promptFor = (a: Article | null) =>
  a?.promptSlug ? PROMPTS.find((p) => p.slug === a.promptSlug) ?? null : null;
