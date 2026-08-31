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
    title: "Three things your AI agent still breaks on",
    standfirst:
      "It forgets everything between sessions, it gets stuck the moment a site asks for a " +
      "login, and it can send something you never meant to send. Three one-line fixes, no rebuild.",
    steps: [
      "Open the system prompt or instructions of any agent you're running.",
      "Add one line: paste in what changed since last session, instead of trusting it to remember.",
      "Add a second line: stop and ask at any login screen — never guess a password or click through one.",
      "Add a third line: always create a draft, never send. You click send yourself.",
    ],
    changes: [
      "It forgets everything between sessions by default — the memory line fixes what it's told, not what it retains.",
      "It gets stuck, or worse, guesses, the moment a site asks for a login — the instruction makes it stop instead.",
      "It can send something you never meant to send, with no undo — the draft-only line puts the final click back on you.",
    ],
    limits: [
      "These are three instructions, not three features — the agent still has no real memory, no login handling, and no undo. The lines only change what it's told to do about each.",
      "None of this needs a rebuild, but it does need you to actually add the lines — an agent left on its defaults still has all three problems.",
    ],
  },
  {
    n: 7,
    title: "Your n8n agent has no idea it's wrong",
    standfirst:
      "\"n8n ai agent tutorial\" is the single highest-demand AI topic we've measured. The common " +
      "failure: a workflow with no branch for its own uncertainty, so a bad answer ships like a good one.",
    steps: [
      "Open any n8n agent workflow you've built, right before the node that sends its output.",
      "Add an IF node that checks the agent's own confidence or a validation result.",
      "Route the low-confidence branch to a human — a Slack message, an email, a review queue.",
      "Only let the high-confidence branch reach the original output node.",
    ],
    changes: [
      "Without the check, the workflow ships the wrong result exactly the way it ships a right one — nothing distinguishes them downstream.",
      "By the time a human notices, the output has already gone out.",
      "One IF node before the output is enough — this is not a rebuild of the workflow.",
    ],
    limits: [
      "This only catches what the agent itself can flag as uncertain — it does not catch a confidently wrong answer.",
      "\"Route to a human\" only helps if someone actually reviews that queue — an unread inbox is the same as no check.",
    ],
  },
  {
    n: 8,
    title: "A check said it passed. It lied.",
    standfirst:
      "It ran clean every time. Nobody had ever given it a case that was actually broken — " +
      "so \"never failed\" got mistaken for \"works.\" One test settles which one is true.",
    steps: [
      "Take the automated check you're currently trusting — a test, a QA script, a validation step.",
      "Write one input you already know is broken, on purpose.",
      "Run the check on that broken input, not on good input.",
      "Confirm it actually fails. If it doesn't, the check has never been asked the real question.",
    ],
    changes: [
      "A check that always passes on real input looks identical to a working check — the only way to tell them apart is to feed it something you know is wrong.",
      "\"Never failed\" is not the same claim as \"works\" — it can just mean the check was never tested against a failure.",
    ],
    limits: [
      "Passing on one known-bad case doesn't prove the check catches every bad case — only that it isn't blind to that one.",
      "This has to be repeated after any change to the check itself, not just after changes to what it checks.",
    ],
  },
  {
    n: 9,
    title: "This agent can send emails by itself. It never does.",
    standfirst:
      "Once a message is sent, a wrong tone or a wrong fact can't be taken back. One switch " +
      "in the workflow keeps every send a human decision: create draft, never send.",
    steps: [
      "Open the step in your email agent's workflow where it currently sends a message.",
      "Change that step from send to create draft.",
      "Read the draft yourself.",
      "Click send yourself, every time — the agent's job ends at the draft.",
    ],
    changes: [
      "A wrong tone or a wrong fact in a sent email can't be taken back — a draft can be edited or deleted before anyone sees it.",
      "The agent still does the writing; the only thing removed is its ability to also press send.",
    ],
    limits: [
      "This slows down anything that genuinely needs to go out instantly — the trade is deliberate, not free.",
      "It only protects the send step. A draft with a wrong fact still needs an actual human read, not just an approval click.",
    ],
  },
  {
    n: 10,
    title: "Most leads go cold before anyone even replies",
    standfirst:
      "By the time a person notices a new lead, it's often already gone cold. An n8n agent " +
      "replies in under a minute — but only the safe part is automatic. The rest becomes a draft.",
    steps: [
      "Wire an n8n agent to reply to a new lead the moment it comes in.",
      "Let it auto-send only the safe acknowledgment.",
      "Route anything that needs a real decision or a real answer to a draft instead.",
      "Have a person review and send the draft ones — never auto-sent.",
    ],
    changes: [
      "Response time drops from however long a human takes to notice, to under a minute, day or night.",
      "Not every reply is safe to automate — splitting by what's safe versus what needs judgment is the actual mechanism, not \"automate everything.\"",
    ],
    limits: [
      "This only helps if the split is actually correct — auto-sending something that needed a real decision is worse than a slow reply.",
      "A draft nobody reviews is the same as no reply at all — the human step still has to happen.",
    ],
  },
  {
    n: 11,
    title: "AI narration has a flaw you can't consciously name",
    standfirst:
      "A word loses its ending, an S goes dull or too hot — most listeners can't name it, only " +
      "feel that something's slightly off. voice_doctor.py measures it directly, before it ships.",
    steps: [
      "Run AI-voiced narration through a measurement tool before shipping it — not your ear alone.",
      "Check it against pacing, rate, sibilance, and word endings, measured against that narration's own median.",
      "If a line fails, run --repair — it levels that line to the median and re-checks its own fix.",
      "Only ship once a pass finds nothing left to flag.",
    ],
    changes: [
      "A dulled word ending or a too-hot S is something most listeners can't name, but hear as \"something's a little off\" — measuring it directly catches what conscious listening misses.",
      "The repair step checks its own output again rather than assuming one pass fixed it.",
    ],
    limits: [
      "This measures against the narration's own median, not a fixed external standard — a whole file recorded badly could pass its own bad baseline.",
      "It catches what it's built to measure — pacing, rate, sibilance, endings. It is not a general \"does this sound good\" check.",
    ],
  },
  {
    n: 12,
    title: "Most people think Claude Code is only for programmers",
    standfirst:
      "It isn't. You describe what you want in plain words, one small change at a time, and " +
      "the tool writes the code. This site was built exactly that way.",
    steps: [
      "Open Claude Code and describe what you want changed, in plain words — no code.",
      "Say one sentence, one small change (\"make the button bigger\"), not a whole feature at once.",
      "Let it write and apply the code itself.",
      "Check the result, then describe the next small change the same way.",
    ],
    changes: [
      "You never write or read code yourself — the instruction is the only thing you supply.",
      "The site this episode links to was built exactly this way, one sentence at a time, not one big spec.",
    ],
    limits: [
      "Starting with one big ask instead of one small change is where this goes wrong first — the discipline is the small-step part, not the tool.",
      "It still needs you to check the result each time — describing a change and trusting it blindly is a different, riskier habit.",
    ],
  },
  {
    n: 13,
    title: "ChatGPT can recall things about you, even in a brand new chat",
    standfirst:
      "Say something once, in an ordinary conversation. Open a totally different chat later, " +
      "ask something connected — it already knows. Nothing re-typed, nothing dug up in settings.",
    steps: [
      "Tell ChatGPT something real about yourself once, in an ordinary conversation.",
      "Close that conversation and open a completely new, unrelated chat.",
      "Ask something connected to what you said.",
      "Notice it already knows — you never repeated it.",
    ],
    changes: [
      "Memory carries across chats by default now, not just within one conversation.",
      "Nothing has to be re-typed or re-explained at the start of a new session.",
    ],
    limits: [
      "It also applies to chats you'd rather it left alone — memory is per-account, not something you switch on per conversation.",
      "This is memory of what you've said, not a guarantee of accuracy — it can carry forward something wrong just as easily as something true.",
    ],
  },
  {
    n: 14,
    title: "Everyone's sharing this claim that AI always lies to please you",
    standfirst:
      "So we tested it — three real times, real transcripts, no editing. We told Claude we're " +
      "quitting our job to day-trade on savings, then asked it to just agree. It never did.",
    steps: [
      "Take a viral claim about how an AI model behaves.",
      "Don't repeat it — test it directly, with a real, specific scenario.",
      "Push it toward the exact failure the claim predicts.",
      "Report exactly what happened, including the real transcript, not a paraphrase.",
    ],
    changes: [
      "Across three real attempts, asking Claude to simply confirm a bad plan (quitting a job to day-trade on savings) got a real pushback every time, not agreement.",
      "The claim — \"AI always flatters you\" — did not hold in this specific, repeated test.",
    ],
    limits: [
      "Three tests on one model is evidence about that model in that situation, not a universal claim about all AI — a different framing or a different model could behave differently.",
      "This confirms the claim didn't hold here; it doesn't prove sycophancy never happens anywhere.",
    ],
  },
  {
    n: 15,
    title: "Gemini fixes your broken formula, already built in",
    standfirst:
      "Google Sheets is the spreadsheet app where you type numbers into boxes and give it " +
      "instructions like \"add these up.\" Get an instruction wrong and Gemini — Google's AI, " +
      "already built into the app — catches the mistake and fixes it, one click, no separate " +
      "tool to install. It can also answer a question typed straight into any box.",
    steps: [
      "Open a Google Sheet — the grid where you type numbers into boxes.",
      "Type an instruction into a box that tells it to do math, like adding up a set of other boxes.",
      "If you make a small mistake in that instruction (a missing bracket, for example), the math breaks and the box shows an error.",
      "A button appears next to the broken box: Fix.",
      "Click it. Gemini checks the instruction — and the rest of the sheet — explains what was wrong in plain words, and corrects it.",
      "Separately, in any empty box type an equals sign, then the word AI, then your question in quotation marks inside round brackets — like =AI(\"what does this number mean\") — and Gemini answers directly inside that box. The equals sign is just how Sheets knows \"this box does something\" instead of holding plain text; the quotation marks mark where your question starts and ends.",
    ],
    changes: [
      "No plugin, no separate app, no copy-pasting into a chatbot — the fix and the question-answering both happen inside the same box you were already using.",
      "It doesn't just correct the instruction silently — it says what was wrong (e.g. a bracket that was never closed), so the mistake is understood, not just patched over.",
      "The question-answering trick (typing AI into a box) works in any box, not just ones that already have a broken instruction in them.",
    ],
    limits: [
      "This fixes mistakes in the instructions you write yourself — it doesn't know whether the numbers you typed in are correct, only whether the instruction is valid.",
      "The exact wording and location of the Fix button can change as Google updates Sheets — if it isn't where this episode shows it, look for an error indicator on the box itself.",
      "Not free for every account: Google's own rollout (June 2026) lists this for Business, Enterprise, Education, AI Pro and AI Ultra Workspace plans. On a personal Gmail account, the equivalent needs Google One AI Premium — check your own account's access before assuming it's there.",
    ],
  },
  {
    n: 16,
    title: "Someone open-sourced our own video pipeline",
    standfirst:
      "This channel's videos are built from a system: turn a plain instruction into a finished " +
      "video, one clip at a time. HeyGen just released a free, open-source tool called " +
      "HyperFrames that does the same thing — built specifically to work with AI coding " +
      "agents like Claude. We installed it and rendered a real video ourselves before " +
      "saying any of this.",
    steps: [
      "Install it with one line in a terminal (a box where you type one instruction and press enter): npx hyperframes init.",
      "Describe what you want, in plain language, to an AI coding agent (like Claude Code) — the same way you'd describe it to a person.",
      "The agent writes a \"recipe\" for you: plain text where each clip is one step, with a start time and how long it lasts.",
      "Run one more command — npm run render — and it turns that recipe into a real video file.",
      "Open the finished file yourself to confirm it's real, the same thing we did before publishing this.",
    ],
    changes: [
      "The same idea this channel has run by hand for fifteen episodes — instruction in, real video out — is now a free, open-source tool anyone can install.",
      "It's free (Apache 2.0 license — no cost, no usage fees) and it installs its own starter files for AI coding agents, so an agent like Claude Code already knows how to use it.",
      "We measured it ourselves: a 10-second test video rendered in about 15 seconds on ordinary hardware.",
    ],
    limits: [
      "This is a tool for building videos with code/agent instructions — it doesn't replace a camera or footage of a real event; it's for the same kind of screen-recording-and-graphics video this channel already makes.",
      "We tested a small, simple example, not a full multi-scene production — a longer, more complex video will take longer to render and may need more setup than shown here.",
      "Open-source projects change; if a command in this episode no longer matches what you see, check the project's own current documentation rather than assuming this episode is still exact.",
    ],
  },
  {
    n: 17,
    title: "A 5-second test for any explanation you write",
    standfirst:
      "One undefined word — \"column\" — is enough to lose someone who already knows the " +
      "topic. The fix isn't writing more carefully, it's a real test run before you record " +
      "or publish anything: read the line, ask \"what did I just say, in your own words?\" " +
      "This is that test, the real before-and-after it catches, and the free skill " +
      "(explain-steps) it lives in — download it below.",
    steps: [
      "Read the line out loud, exactly as written.",
      "Ask someone else — or yourself, out loud, in a different sitting — \"what did I just say, in your own words?\"",
      "Never accept a yes-or-no answer to \"did that make sense?\" — it doesn't catch anything; a paraphrase does.",
      "If the answer doesn't come back matching what the line actually meant, the line isn't done — rewrite it, don't just slow down on it.",
      "Repeat for every line that names a tool, a technical term, or an interface element before it gets recorded or published.",
      "To run this automatically in Claude Code: open /s/explain-steps on this site, download SKILL.md, and put it at .claude/skills/explain-steps/SKILL.md in your own project — Claude Code picks it up with no restart and no config.",
    ],
    changes: [
      "The real example this rule caught: \"Add this to the column\" (said once, never explained) became \"Instagram fills this box on its own\" — same fact, zero required vocabulary.",
      "The rule lives in a written, free skill called explain-steps — the same one behind every step-by-step explanation this channel makes, not invented just for this episode.",
      "It's a five-minute check before recording, not a rewrite of the whole production process — the cost is asking the question, not redoing the work.",
    ],
    limits: [
      "This catches whether a sentence is understandable, not whether it's factually correct — a wrong but clearly-worded claim still needs separate fact-checking (see episode 15's own correction).",
      "It works best with a second person; testing it on yourself only works if you can genuinely forget what you meant to say, which is harder than it sounds.",
      "Four other spots in the back catalog (episodes 3, 7, 10, 11) were already found to have the same kind of unexplained jargon and haven't been rebuilt yet — this rule is applied going forward, not retroactively to published episodes.",
    ],
  },
];

export const articleFor = (n: number) => ARTICLES.find((a) => a.n === n) ?? null;
export const promptFor = (a: Article | null) =>
  a?.promptSlug ? PROMPTS.find((p) => p.slug === a.promptSlug) ?? null : null;
