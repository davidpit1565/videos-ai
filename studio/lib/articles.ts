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
      "Find where your agent's starting instructions live — that's what \"system prompt\" means, the text it reads before your first message. In ChatGPT: Settings → Personalization → Custom instructions. In n8n or a similar builder: the agent node's own \"System Message\" field.",
      "Add one sentence, word for word: \"If you're not sure, say so instead of guessing.\"",
      "Save it.",
      "Give the agent a task where the honest answer is \"I don't know\" or \"this failed\" — something you already know it can't actually do.",
      "Read exactly what it says back — not what it does next, what it reports.",
      "If it still claims success on that failure, the line changed its wording, not the underlying problem — that's a real result, not a broken test.",
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
      "Find where your agent's starting instructions live (its \"system prompt\" — the text it reads before your first message). In ChatGPT: Settings → Personalization → Custom instructions. In n8n or Make: the agent node's own \"System Message\" field.",
      "Add: \"At the start of each session I'll tell you what changed since last time — don't assume you remember on your own.\"",
      "Add a second line: \"If a site asks you to log in, stop and ask me — never guess a password or click through a login screen yourself.\"",
      "Add a third line: \"Always create a draft. Never send anything yourself — I'll click send.\"",
      "Save, then test each one on purpose: point it at a login-walled page and give it something to send, and confirm it stops both times instead of acting.",
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
      "Open the n8n workflow with your AI Agent in it, and find where its output currently connects straight into the next step (the one that sends or saves the result).",
      "In the node panel on the left, search \"If\" and drag an IF node — n8n's branching block, one input and two outputs (\"true\" / \"false\") based on a condition you set — onto the canvas between the Agent and that next step.",
      "Delete the direct wire from the Agent to the next step, then wire the Agent's output into the IF node instead.",
      "Set the IF node's condition to check whatever tells you the answer might be shaky — a confidence field the Agent already outputs, or a plain rule like \"is this field empty.\"",
      "Wire the IF node's \"true\" output (the low-confidence branch) to a Slack message, an email node, or wherever a person will actually see it — not back into the original flow.",
      "Wire the \"false\" output (the confident branch) into the same next step that was connected before.",
      "Run the workflow once with a case you expect to be low-confidence, and confirm it lands with a person instead of going straight out.",
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
      "Find the exact step in your email agent's workflow that sends the message — in n8n this is usually a \"Send Email\" or Gmail/Outlook node; in Zapier or Make, the final email action in the flow.",
      "Open that step and change its action from \"Send\" to \"Create Draft\" — most email nodes have Draft sitting in the same dropdown as Send.",
      "Run the workflow once and check that account's Drafts folder yourself, to confirm it actually landed there instead of going out.",
      "Read the draft yourself before doing anything else with it.",
      "Click send yourself, from your own inbox, every time — the workflow's job now ends at the draft.",
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
      "In n8n, connect your lead-intake trigger (a form submission, a new CRM record, a webhook) directly into an AI Agent node that drafts the reply.",
      "Right after the Agent, add an IF node (n8n's branching block — search \"If\" in the node panel) that checks whether the reply is a safe acknowledgment (\"thanks, someone will follow up\") or something needing a real decision (a price, a yes/no, a specific answer).",
      "Wire the \"safe\" branch straight into a Send Email node — this one goes out automatically, with no review.",
      "Wire the \"needs judgment\" branch into a Create Draft step instead of Send — same fix as episode 9.",
      "Have a real person check that drafts folder on a schedule — a draft nobody reads is the same as no reply at all.",
      "Test it with two example leads: one where a plain acknowledgment is genuinely enough, one where it clearly isn't — confirm each one takes the branch it should.",
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
      "Open a terminal (a text window where you type a command and press enter) in the folder that has your narration file and voice_doctor.py.",
      "Type: python3 voice_doctor.py your-narration-file.wav — and press enter.",
      "Read the report it prints: pacing, rate, sibilance (how harsh the S sounds are), and word-ending strength, each measured against that same file's own average line, not a fixed outside standard.",
      "If a line is flagged, run it again with the repair option: python3 voice_doctor.py your-narration-file.wav --repair fixed-file.wav — this levels just that line to match the rest.",
      "Run the same check again on the repaired file, to confirm the flag is actually gone, not just quieter.",
      "Only ship once a run comes back with nothing left flagged.",
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
      "This rule caught real gaps in the back catalog too (episodes 3, 6, 7, 9, 10, 11 all had unexplained jargon or steps too vague to actually follow) — those have since been rewritten to the same standard, not left as an exception.",
    ],
  },
  {
    n: 18,
    title: "ChatGPT can use a website now",
    standfirst:
      "ChatGPT Work — the mode next to Chat — reads through real websites on its own " +
      "instead of just describing what to do, and comes back with a finished result. " +
      "Ask it to compare a few pricing plans and it hands you a spreadsheet, not a " +
      "suggestion to go check yourself. Verified before publishing, including the " +
      "rename: this used to ship as a separate \"agent mode,\" which OpenAI retired in " +
      "early August 2026 in favor of Work — an episode about the old name would already " +
      "be wrong.",
    steps: [
      "Open ChatGPT and switch from \"Chat\" to \"Work\" — the mode picker sits right next to where you type your message.",
      "Give it one concrete task with a clear finish line — \"compare these 3 plans and tell me the cheapest\" — not an open-ended one.",
      "Let it run: it's not instant — a real task can take a while, sometimes hours, not seconds.",
      "Watch the first run all the way through before handing it a second task unsupervised.",
      "Don't give it anything that needs you to already be logged into an account somewhere — that's not what it's built to do.",
    ],
    changes: [
      "The real limit, verified before publishing: it won't log into an account for you — it works with public pages, not ones behind your own sign-in.",
      "It's genuinely slow by design — built to stay with a task for a long stretch, not to answer in seconds.",
      "It's not a separate unlimited add-on: usage comes out of your existing plan (Plus or Pro), not a special extra quota.",
    ],
    limits: [
      "This is for tasks with a clear, checkable finish line (compare, look up, summarize across a few pages) — not open-ended research or anything where a wrong answer is costly and hard to catch.",
      "It won't act inside an account you're already signed into — a task needing that isn't a fit for it.",
      "Names and limits in this space change fast — OpenAI retired the previous \"agent mode\" without much notice days before this episode was recorded; check ChatGPT's own current mode picker if this episode is more than a few months old.",
    ],
  },
  {
    n: 19,
    title: "Claude keeps your files now",
    standfirst:
      "A Claude Project carries your uploaded files and written instructions into " +
      "every new chat you open inside it — no re-explaining, no re-uploading. Verified " +
      "before publishing: twenty files per project, five megabytes each, and files " +
      "stay scoped to the project you added them to — they don't follow you into a " +
      "different one.",
    steps: [
      "Open Claude and start a new Project (not a regular chat) — the option sits alongside your chat list.",
      "Upload the files this work actually needs, and write your instructions once in the project's own instructions field.",
      "Open a new chat from inside that project whenever you come back to the same work — it already has your files and instructions, nothing to re-paste.",
      "Keep unrelated work in a separate project — files and instructions don't cross over between projects automatically.",
      "If you hit the file limit, remove what the current chat doesn't need rather than starting a new project just to fit one more file.",
    ],
    changes: [
      "The real cap, verified before publishing: twenty files per project, five megabytes each.",
      "It won't share files with a project you didn't add them to — each project's files stay scoped to that project.",
      "It's not a chat you keep alive in the background — the saving is in not re-explaining or re-uploading each time you return, not in the project itself doing anything while you're away.",
    ],
    limits: [
      "This fits recurring work with the same files and instructions — a one-off question doesn't need a project.",
      "Files still count toward the model's context the same as anything else — a project doesn't make your files free to include.",
      "Anthropic's own limits here can move — check Claude's current project settings if this episode is more than a few months old.",
    ],
  },
  {
    n: 20,
    title: "ChatGPT was going to buy things for you",
    standfirst:
      "OpenAI's Instant Checkout promised a purchase without ever leaving the chat. " +
      "Six months after launch, it's retired: fewer than fifteen of Shopify's millions " +
      "of merchants ever turned it on. Verified before publishing — what's left is " +
      "product discovery, not purchase; ChatGPT finds what you want and hands you a " +
      "link, the same as a search engine always did.",
    steps: [
      "Ask ChatGPT to find or compare a product the way you'd ask a search engine.",
      "Expect a recommendation and a link out to the merchant's own site or app — not a completed purchase inside the chat.",
      "Do the actual checkout (payment, shipping, account login) on the merchant's own page, same as any other online purchase.",
      "Don't build a workflow around \"buy it in ChatGPT\" — that specific feature (Instant Checkout) is retired.",
    ],
    changes: [
      "The real number, verified before publishing: fewer than fifteen of Shopify's millions of merchants ever turned Instant Checkout on before it was retired.",
      "Buying inside ChatGPT converted at roughly a third the rate of sending the same shopper straight to the merchant's own site.",
      "What's left is discovery, not purchase — the same shape as a search engine's results page, not a new capability.",
    ],
    limits: [
      "This isn't a criticism of ChatGPT generally — it's one specific, named feature (Instant Checkout) that launched and was retired within about six months.",
      "Agentic checkout hasn't disappeared industry-wide — other players (Google, Perplexity) have their own versions; this episode covers what ChatGPT itself does today, not the whole category.",
      "Check ChatGPT's own current shopping behavior if this episode is more than a few months old — this space is changing fast.",
    ],
  },
  {
    n: 21,
    title: "Can an AI browser actually run your errands?",
    standfirst:
      "A real test, not a demo: 300 everyday tasks across 136 real websites. The " +
      "strongest AI browser agent finished 61.3% of them; most agents landed near " +
      "30%. A person handed the same list clears almost all of it. Perplexity's " +
      "Comet browser is the one worth actually trying — free, on every platform, " +
      "and honest about what still breaks it.",
    steps: [
      "Go to perplexity.ai/comet and click \"Get Comet\" — it's a small, fast download (about 13MB), free, no account required to start.",
      "Open the downloaded file and install it, same as any other browser (Chrome, Edge).",
      "On first launch, sign in with a free Perplexity account, or create one.",
      "Comet will offer to import your existing browser's history, bookmarks and passwords — this step is optional, the browser works without it.",
      "Open the Comet Assistant (the sidebar panel — its exact icon/label can shift between versions, so if it's not obvious, check Comet's own onboarding tour, which points it out).",
      "Type a real task in plain English — e.g. \"find a flight from my city to London next weekend and show me the three cheapest options.\"",
      "Watch it work: Comet shows each step it takes as it browses, not just a final answer — you can stop or correct it mid-task.",
      "Start with a short, one-destination task before trying anything with multiple steps chained together — that's exactly where it's most likely to break (see Limits).",
    ],
    changes: [
      "The real number, from an independent test across 136 real websites: the strongest AI browser agent completed 61.3% of 300 everyday tasks; most agents scored closer to 30%.",
      "A human given the identical list of tasks completes nearly all of them — the gap between that and even the best agent is the part a product demo never shows.",
      "Comet's free tier already includes agentic browsing (form-filling, shopping, multi-step workflows) — this isn't a paywalled preview feature.",
    ],
    limits: [
      "It does not reliably chain many steps together — a wrong turn early in a long task compounds, and everything after it goes wrong too. Shorter, single-purpose tasks are where it's actually reliable today.",
      "A paid \"background assistant\" tier exists for running tasks without watching them live — the free tier expects you to stay present and check in.",
      "This episode names one specific browser (Comet) and one specific benchmark, both current as of publishing — re-check both if this episode is more than a few months old; this category is moving fast.",
      "Not a security review: agentic browsers as a category have documented risks around a malicious page hijacking an agent's actions — this episode doesn't cover that side, only whether the everyday-task claim holds up.",
    ],
  },
  {
    n: 22,
    title: "n8n's AI Agent can lie to you — and still show green",
    standfirst:
      "In n8n, when an AI Agent calls a tool and that tool fails, the Agent itself can " +
      "still finish green. Real, open, unresolved on n8n's own GitHub. We built one: " +
      "one agent, one tool, one deliberately broken key. The tool failed. The dashboard " +
      "called it a success — because n8n's own error trigger alone doesn't catch this.",
    steps: [
      "Quick term check: in n8n, a \"node\" is one block in your workflow — you drag it in from the panel on the left and wire it to the blocks before and after it. Every \"node\" below is one of these blocks.",
      "This fix has two parts — a workflow-level error trigger alone does not catch this, because the AI Agent resolves the failure internally before the workflow ever \"errors.\" Both parts are needed.",
      "Part 1 — make every tool report its own status honestly. Open each Tool node your AI Agent calls. For an HTTP Request tool, go to Options → Response and enable \"Never Error\" — this stops the tool from throwing silently and lets you inspect what actually happened instead.",
      "For a Code node or sub-workflow used as a tool, wrap its logic so it always returns one structured object instead of throwing: {\"status\": \"ok\" | \"failed\" | \"empty\", \"data\": ...} — a plain success/failure field the next step can actually read.",
      "Part 2 — add a real check after the Agent. Add an IF node (or a Code node) directly after your AI Agent node.",
      "In that node, check the Agent's own output for the failure signs: any tool result where status equals \"failed\", a tool missing entirely from the Agent's intermediate steps, or a result with zero items where you expected real data.",
      "Route the \"broken\" branch of that IF node into a Stop And Error node — this is what actually makes the workflow fail for real, instead of silently continuing on bad data.",
      "Only now does the standard fix apply: create a small separate workflow starting with an Error Trigger node (no configuration needed) — this is where you add a Slack/email/Discord alert.",
      "In your main workflow (the one with the Agent), open the three-dot menu → Settings → Error Workflow, and select the error-handler workflow you just made. Save.",
      "Test it honestly: temporarily break one tool on purpose (a wrong API key works well) and run the workflow for real. If you did this right, you get an actual alert — not a quiet green checkmark.",
    ],
    changes: [
      "A real, sourced defect: n8n's own GitHub has two separate open issues on this (#22771, #24042), and an active 2026 community thread from someone already on n8n's latest version — this isn't a stale, already-fixed bug.",
      "n8n treats a tool's failure as part of the AI Agent's own reasoning process, not as a workflow execution error — so the built-in Error Workflow mechanism never fires on its own, no matter how it's configured.",
      "The real fix isn't the Error Trigger alone — it's making every tool report status honestly, checking that status right after the Agent, and deliberately throwing before anything destructive happens.",
    ],
    limits: [
      "This is a design characteristic of n8n's current AI Agent node, confirmed as unresolved as of this episode's publishing (one fix proposal was closed \"not planned\" in March 2026) — re-check n8n's own GitHub if this episode is more than a few months old.",
      "The fix adds real setup work per tool, per agent — it does not come free, and skipping it on even one tool leaves that one silent.",
      "This episode covers one specific, documented failure mode (a tool call failing silently inside an Agent) — not a general audit of n8n's reliability.",
    ],
  },
  {
    n: 23,
    title: "22 episodes in, one file keeps this from breaking",
    standfirst:
      "Claude Code reads one file — CLAUDE.md — the moment it opens a project folder, and " +
      "every new session starts already knowing the rules. This channel runs on one: a real " +
      "rule for each of its costliest mistakes, including a metric that measured position on " +
      "screen instead of the actual sound, and a check that ran before the fix it was " +
      "supposed to protect. Neither was caught by a tool. Both are one line in the file now.",
    steps: [
      "Open your terminal — on Mac, search \"Terminal\" with Spotlight (the magnifying glass, top right); on Windows, search \"PowerShell\" in the Start menu. Both come built into the OS already, nothing to download for this step.",
      "Mac, Linux or WSL: paste curl -fsSL https://claude.ai/install.sh | bash and press Enter. Windows PowerShell: paste irm https://claude.ai/install.ps1 | iex instead and press Enter. This installs Claude Code itself — no separate Node.js install needed.",
      "When it finishes, type claude --version and press Enter. If it prints a version number back, the install worked — if it says \"command not found,\" close and reopen the terminal window first before trying again.",
      "Move into the project you want Claude Code to work on: type cd followed by a space and the folder's path, then press Enter — for example cd Documents/my-project.",
      "Type claude and press Enter. This opens a Claude Code session inside that exact folder — the folder you're in when you type this is the one it will read rules from.",
      "In that same folder, create a new plain-text file named exactly CLAUDE.md (capital letters exactly as shown, no other extension) — any text editor works, including opening it with your editor of choice or running code CLAUDE.md if you use VS Code.",
      "Write one real rule per line, in plain English, for a mistake that has actually already happened in this project — not a wishlist of things that might. \"Never delete the backup folder\" is a real rule; \"write clean code\" is not specific enough to catch anything.",
      "Save the file, close the current Claude Code session, and start a fresh one with claude in the same folder — it reads CLAUDE.md automatically this time, before you type a single instruction.",
      "Optional, to confirm it actually worked: ask it directly, \"what rules are in CLAUDE.md?\" — a working setup quotes the rules back without you pasting the file into the chat.",
    ],
    changes: [
      "Claude Code reads a file named exactly CLAUDE.md, sitting in a project's top folder, automatically on every session start — no flag, no pasted reminder, no re-explaining.",
      "The current native install command (checked today): curl -fsSL https://claude.ai/install.sh | bash on Mac/Linux/WSL, or irm https://claude.ai/install.ps1 | iex on Windows PowerShell — no Node.js required either way.",
      "This is not a hypothetical benefit — this exact channel's own CLAUDE.md carries a real rule for each of its three costliest production mistakes, written the same day each one was found.",
    ],
    limits: [
      "The file only helps if it names real, specific mistakes — a vague wishlist (\"write good code,\" \"be careful\") gives an agent nothing concrete to check itself against.",
      "It's read once at session start, not enforced like a lint rule — nothing physically stops an agent from breaking a written rule anyway. What it removes is the excuse of not knowing the rule existed, not the possibility of a mistake.",
      "The exact install command shown here can change as Claude Code updates — re-check code.claude.com/docs if this episode is more than a few months old.",
    ],
  },
  {
    n: 24,
    title: "Editors squeeze the picture to fit the audio. We do the opposite",
    standfirst:
      "Every video editor squeezes the picture to fit a fixed length, then stretches the " +
      "narration to fit inside it. This channel's own render pipeline (retime.py) does the " +
      "opposite: it builds the narration first, at its own natural pace, and moves every " +
      "cut, caption and on-screen beat to match the voice's real pauses. One real episode " +
      "measured a 0.60-second overlap from the old way; the technique that fixed it works " +
      "by hand, in any editor, without any special software.",
    steps: [
      "Record or generate your full narration first, as one continuous audio file — before you touch the video timeline at all. This is the one thing that has to change first: the voice comes before the picture, not after.",
      "Open your editor (this works the same in CapCut, DaVinci Resolve, or Premiere) and drop only that audio file onto its own track. Don't add any video clips yet.",
      "Zoom in on the timeline until you can see the actual waveform — the audio track's shape, not just a flat bar. Every editor shows this by default once you zoom in far enough.",
      "Look for the real gaps: flat, near-silent sections in the waveform between sentences. These are the natural pauses your voice actually took, not a fixed number of seconds.",
      "Use the Split tool (in CapCut, tap the audio clip then tap the split icon; in Premiere or Resolve, the razor tool, keyboard shortcut C) and place a cut at the start of each real gap you found — not at a round number like \"every 3 seconds.\"",
      "Now bring in your video clips, one per section of narration. Drag each clip's edge to line up with the cuts you just placed in the audio, so the picture changes exactly where the voice actually pauses.",
      "If a video clip is a little short or long for its section, trim the clip itself to fit the gap — never speed up or stretch the audio to fit a video length you picked first. The audio's real timing is the one thing that shouldn't move.",
      "Play it back. The tell that this worked: no sentence gets cut off, and no scene change happens while someone is still mid-word.",
    ],
    changes: [
      "The core reversal: build narration at its natural pace first, then move the picture's cuts to match its real pauses — not the other way around.",
      "A real, measured bug this fixed: one published episode had two lines of narration overlapping by 0.60 seconds because the old pipeline stretched a line up to 12% to force it into a fixed slot.",
      "A second real bug: an episode once cut off mid-word because the pipeline's own measurement of where a line \"ended\" undercounted a slow trailing word — fixed by using the actual audio file's real length as a floor, never a guess.",
      "The technique itself needs no special software — a waveform view and a split tool, which every mainstream video editor already has, is enough to do this by hand.",
    ],
    limits: [
      "This does not fix a bad recording — if the narration itself is rushed or unclear, matching cuts to its pauses just preserves that pacing exactly as-is.",
      "Doing this by hand, clip by clip, is slower than a fixed-slot template — the payoff is fewer overlaps and cut-off words, not less editing time.",
      "This channel's own version (retime.py) automates the matching across an entire script at once; doing it manually in a general editor means finding each gap yourself, one at a time.",
    ],
  },
];

export const articleFor = (n: number) => ARTICLES.find((a) => a.n === n) ?? null;
export const promptFor = (a: Article | null) =>
  a?.promptSlug ? PROMPTS.find((p) => p.slug === a.promptSlug) ?? null : null;
