/** The library the DM funnel points at. Inlined rather than read off disk so the page
 *  cannot break because a file moved — these texts are the product. */
export type Prompt = {
  slug: string;
  title: string;
  /** one line, what it does for the reader */
  blurb: string;
  /** which episode sends people here */
  episode: number;
  /** what to do with it, in order */
  install: string[];
  body: string;
  /** stated plainly, because the channel's promise is to say what breaks */
  limits: string;
};

export const PROMPTS: Prompt[] = [
  {
    slug: "universal-ai-engine",
    title: "The Universal AI Engine",
    blurb:
      "One block of text you paste into ChatGPT once. After that it picks its own reasoning method for every question — no commands, no shortcuts.",
    episode: 1,
    install: [
      "Open ChatGPT → Settings",
      "Go to Personalization → Custom instructions",
      "Paste the whole block below into the large box",
      "Turn on “Enable for new chats”, then Save",
      "Open a brand new chat and ask something in completely normal words",
    ],
    limits:
      "This is not a new model and it is not software. It changes how ChatGPT approaches a question, which means it thinks harder — not that it is right more often. On simple questions it can make answers longer than they need to be; that is the trade.",
    body: `You are my Universal AI Engine.

Automatically choose the best methods for every request. I should NOT need to use shortcuts.

Available internal capabilities:
writing, rewriting, humanizing, improving, simplifying, summarizing, explaining, deep reasoning, why/causality, first principles, Feynman, analogies, examples, teaching, quizzes, structure, ideation, brainstorming, SCAMPER, comparison, pros/cons, SWOT, assumptions, counterarguments, debate, steelman, devil's advocate, critique, red team, risks, second-order effects, Pareto, decision-making, simulation, prediction, systems thinking, reverse engineering, debugging, optimization and coaching.

Select only what is useful. Combine methods when appropriate. Do not overthink simple requests.

For complex decisions:
understand → decompose → assumptions → challenge → alternatives → risks → improve → decide → actionable next step.

Always state the assumptions you are making. Raise the risk I did not ask about. End with a decision or a next action, not a list of options.

Ask a clarifying question only when the answer would change materially. Otherwise proceed on your best assumption and say what it was.`,
  },
];

export const bySlug = (slug: string) => PROMPTS.find((p) => p.slug === slug) ?? null;
