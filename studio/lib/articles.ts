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
  {
    n: 25,
    title: "Your n8n retry doesn't just try again",
    standfirst:
      "n8n workflows default to \"at least once\" delivery: a timeout retry replays the " +
      "whole step, side effects included. Real case: an API call actually finished, but " +
      "the response never came back before the timeout — n8n has no way to know that, " +
      "so the retry fires the same call again. The fix is one idempotency check before " +
      "any external call, not just this one.",
    steps: [
      "Quick term check: an \"idempotency key\" is just a unique ID for one specific attempt at an action. Send it once, and if that same ID shows up again later, you know it's a retry of the same thing — not a new request.",
      "Open the n8n workflow that calls the external API (the send, email, or payment node) and find the node right before that call.",
      "Add a new node before it: click the + button and search for \"Code\". This node's job is to build the key, not send anything yet.",
      "Inside the Code node, build a key from only the data that makes this one attempt unique — for example the order ID, or a hash of the exact request body. The same input must always produce the exact same key, on the first try and on every retry.",
      "Add an IF node right after the Code node, still before the real API call. This is where the workflow decides: has this exact key already gone out?",
      "For the actual lookup, use whatever data store this workflow can already reach — a Google Sheets or Airtable node works, or a database node if one is already wired in. Look up a row matching the key in a \"already sent\" sheet or table.",
      "Wire the IF node's branches: if the key is already found, route to a No Operation (or Stop And Error) node and go no further — it already went out once. If the key is not found, continue on to the real API call node exactly as before.",
      "Right after the real API call succeeds, add one more node that writes the key into that same \"already sent\" store — an Airtable/Sheets \"Create row\" node works. This is what the next retry, if there is one, will find.",
      "Test it honestly: run the workflow twice in a row with the exact same input. The first run should reach the real API call as usual. The second should stop at the IF node and never reach it again.",
    ],
    changes: [
      "n8n's default retry behavior replays the whole step on a timeout, side effects and all — it has no built-in way to know the original call actually succeeded before the response was lost.",
      "The fix isn't specific to n8n or to one node type: any workflow tool that retries on failure needs the same check before any call with a real side effect (sending, charging, creating).",
      "The key has to be deterministic from the input alone — built from data that's already fixed before the first attempt, never from a timestamp or ID generated fresh on each run.",
    ],
    limits: [
      "This protects against an exact retry of the same input — it does not fix a different, genuine failure elsewhere in the workflow.",
      "The lookup step needs a real, persistent store (a Sheet, Airtable, or a database) — n8n's own in-memory workflow data isn't guaranteed to survive a restart on every hosting setup.",
      "Adds one Code node, one IF node, and one write-back node per external call that needs it — it isn't free, and skipping it on even one call leaves that one unprotected.",
    ],
  },
  {
    n: 26,
    title: "This is a real AI model. My WiFi is off.",
    standfirst:
      "No account, no subscription, no API key — a real AI model, running fully offline, " +
      "on a normal laptop with no dedicated graphics card. The tool is Ollama, free and " +
      "open source, and one command installs it. It won't out-argue the biggest paid " +
      "models, but for a real, private, offline assistant, it already works.",
    steps: [
      "A \"terminal\" is just a plain window where you type text commands instead of clicking icons — every Mac and Windows computer already has one built in, nothing to download for this part. Open it — Mac: click the magnifying glass icon top-right of the screen (Spotlight), type \"Terminal\", press Enter; Windows: click the Start menu (bottom-left), type \"PowerShell\", press Enter. A plain black or white window opens — that's it, that's the terminal.",
      "Copy this exact line for your system, paste it into that window, and press Enter. Mac/Linux: curl -fsSL https://ollama.com/install.sh | sh — Windows: powershell -c \"irm https://ollama.com/install.ps1 | iex\". This is the official installer from Ollama's own site (ollama.com) — safe to paste. You'll see several lines of text scroll by as it downloads and installs; when the lines stop and you see a new blank line waiting for input, it's finished — that can take a minute or two, depending on your internet.",
      "Type ollama run llama3 and press Enter. The first time, this downloads the actual AI model (a few gigabytes — needs internet, and can take several minutes depending on your connection). You'll see a progress bar while it downloads. When it's done, the model starts up and the window shows \">>>\" waiting for you to type something — that's it running, fully on this computer.",
      "Optional, if you want to see the \"offline\" claim for yourself: turn off WiFi (or unplug the cable) now, then run ollama run llama3 again in a new terminal window — it still answers, because the model already lives on this machine and never needs the internet again.",
      "Type any question directly after the \">>>\" and press Enter — it answers right there in the same window.",
      "To leave the chat and get your terminal back, type /bye and press Enter.",
      "To try a smaller, faster model instead of llama3: type ollama run phi3 (smaller and faster, less capable) or ollama run gemma2 (a middle ground) — same steps as above, just that name instead of llama3.",
    ],
    changes: [
      "Ollama is free, open source, and actively maintained — confirmed via its own GitHub and release history, not assumed from an old memory of the tool.",
      "Local use needs no account and no API key at all — the model runs entirely on the machine once downloaded, with nothing to send anywhere.",
      "A normal laptop with no dedicated graphics card runs a 7B-class model (Llama 3, Gemma 2, Phi-3) at a usable speed — a GPU helps, but this doesn't require one.",
    ],
    limits: [
      "Ollama separately offers optional paid cloud tiers for cloud-hosted inference — this episode is about the free, local, offline path specifically, not Ollama's whole product line.",
      "A small local model won't match the biggest paid models on hard reasoning tasks — the claim here is a real, private, free, offline assistant, not a like-for-like replacement.",
      "The first ollama run of any model needs an internet connection to download it once — \"offline\" describes every run after that, not the very first one.",
    ],
  },
  {
    n: 27,
    title: "I told Claude Code the wrong bug. On purpose.",
    standfirst:
      "A real, unscripted test: fed Claude Code a deliberately false bug description — " +
      "\"the loop skips one entry, at the top\" — on a script whose real bug was " +
      "somewhere else entirely. It didn't just patch the described symptom; it found " +
      "the actual defect (an operator-precedence mistake one line down) and fixed that " +
      "instead. Comes with a normal Claude Pro plan, $20/month, nothing extra to buy.",
    steps: [
      "A \"terminal\" is a plain window for typed commands — every Mac and Windows computer already has one, nothing extra to download for this part. Open it — Mac: click the magnifying glass icon top-right of the screen (Spotlight), type \"Terminal\", press Enter; Windows: click the Start menu (bottom-left), type \"PowerShell\", press Enter.",
      "Mac/Linux: paste curl -fsSL https://claude.ai/install.sh | bash into that window and press Enter. Windows: paste irm https://claude.ai/install.ps1 | iex instead. This is the official installer from Anthropic's own site — safe to paste. Lines scroll by while it installs; when they stop and you get a new blank prompt, it's done.",
      "Type claude --version and press Enter. If it prints a version number, the install worked — if you see \"command not found\", close the terminal window and open a fresh one (the first install needs a new window to be recognized).",
      "Type claude and press Enter inside any project folder. The first time, a browser tab opens asking to log in with the same email and password used for claude.ai.",
      "Already have a Claude Pro or Max subscription? Nothing else to buy — Claude Code is included at no extra cost. On the free plan, it asks to upgrade before it will run any real request.",
      "Type a real request in plain English, describing what you think is wrong — for example \"there's a bug in this file: it skips the first item in the loop, fix it\" — and press Enter. It reads the actual file itself rather than only trusting the description, so if the real bug is somewhere else, it can find and fix that instead.",
      "Optional: the same tool also works inside VS Code, Cursor, and JetBrains IDEs as a built-in extension, not just the terminal — same login, same account, no separate setup.",
    ],
    changes: [
      "Claude Code is included with a normal Claude Pro subscription ($20/month) — confirmed current via Anthropic's own pricing page before this episode was written, not assumed from an older episode.",
      "It reads the actual file before acting, rather than only trusting a plain-English bug description — a wrong or incomplete description of the symptom doesn't stop it from finding the real defect.",
      "The demo in this episode was run for real, not scripted: a genuinely broken script, a deliberately false bug description, and the tool's own unedited response as the evidence.",
    ],
    limits: [
      "This one test showed the tool looking past a wrong description on one small, clear-cut bug (an operator-precedence mistake) — it isn't a claim that every wrong description gets caught on every bug, especially subtler or more ambiguous ones.",
      "Free-plan accounts can't run this at all without upgrading first — the $20/month claim is specifically about Pro-and-up, not every Claude account.",
      "Needs a real project folder and an actual broken file to point it at — it doesn't diagnose a bug from a description alone with no code to read.",
    ],
  },
  {
    n: 28,
    title: "Four rows started with 'test_'. Only three were.",
    standfirst:
      "A real, unscripted test: a small billing system with a genuine trap — one row " +
      "looks exactly like leftover test data (same id prefix, same shape) but is " +
      "actually a real customer account with a real balance. Told to \"clean up the " +
      "test data,\" Claude Code read the code first, found the real dependency, and " +
      "deleted only the genuine fixtures. Comes with a normal Claude Pro plan, " +
      "$20/month, nothing extra to buy.",
    steps: [
      "Already have Claude Code installed from a previous episode? Skip to step 4. Otherwise: open a terminal (Mac: Spotlight, magnifying glass top-right, type \"Terminal\"; Windows: Start menu, type \"PowerShell\") and paste the install line for your system: Mac/Linux curl -fsSL https://claude.ai/install.sh | bash, Windows irm https://claude.ai/install.ps1 | iex.",
      "Type claude --version and press Enter to confirm it installed, then type claude inside any project folder and log in with your claude.ai email and password when the browser tab opens.",
      "Already have a Claude Pro or Max subscription? Nothing else to buy — Claude Code is included at no extra cost.",
      "Before giving it a real cleanup instruction on anything that matters, work on a copy or a fresh git branch first — type git checkout -b cleanup-test inside the project folder. This makes any outcome reversible: git checkout main undoes everything if the result isn't what you wanted.",
      "Describe the cleanup the way you actually would to a person, not a precise technical spec — for example \"clean up the test data in this file, it's cluttering everything.\" Vague, real language is exactly what this episode tested, on purpose.",
      "Read what it changed before trusting it: type git diff to see exactly which lines it touched. This episode's real result left one row untouched because a comment in the code explained why it wasn't actually test data — the same diff would show you that same reasoning on your own files.",
      "If anything looks wrong, git checkout main throws away the branch and its changes completely — nothing is committed to your real project until you decide it's correct and merge it yourself.",
    ],
    changes: [
      "Claude Code reads the actual code and its comments before acting on a vague instruction — it doesn't blindly pattern-match on something like an id prefix when the code itself explains an exception.",
      "It explicitly avoided making an irreversible-feeling change (deleting a row) on its own judgment when the instruction was ambiguous about that specific case, and said so in its own explanation rather than silently guessing.",
      "The demo in this episode was run for real, not scripted: a genuinely constructed trap (a real customer account with a test-shaped id), a deliberately vague instruction, and the tool's own unedited response as the evidence.",
    ],
    limits: [
      "This one test showed correct judgment on one specific, well-commented trap — it isn't a guarantee that every ambiguous instruction gets caught correctly on every codebase, especially one with no explanatory comments at all.",
      "Free-plan accounts can't run this at all without upgrading first — the $20/month claim is specifically about Pro-and-up, not every Claude account.",
      "Working on a git branch only protects code already in a git repository — it does nothing for a request made directly against a live database or production system with no version control.",
    ],
  },
  {
    n: 29,
    title: "Your n8n workflow can fail completely — and still say 'Success.'",
    standfirst:
      "A real, sourced n8n behavior, verified against n8n's own docs and a dated " +
      "community report: a node's \"On Error\" setting can be set to \"Continue\" so " +
      "a small hiccup doesn't stop the whole workflow — but when that node genuinely " +
      "fails, n8n's Executions list still reads Success. The actual error only shows " +
      "up inside that one node's own output, nowhere else. Free tier and self-hosted " +
      "behave identically — this isn't gated by plan.",
    steps: [
      "Log into n8n (n8n.cloud free tier, or a self-hosted instance — this behaves the same on both) and create a new, empty workflow so nothing real is affected.",
      "Add a Manual Trigger node (the default starting node on a blank workflow), then add an HTTP Request node connected after it.",
      "In the HTTP Request node, set the URL to something guaranteed to fail — a domain that doesn't resolve, or any URL ending in a path you know returns a 404.",
      "Open that same node's Settings tab and find the \"On Error\" field. Change it from \"Stop Workflow\" (the default) to \"Continue\".",
      "Run the workflow (the \"Execute Workflow\" button). Open the Executions list on the left — it reads Success, in green, even though the request actually failed.",
      "Click into that one node's output panel — the real error (fields like error and statusCode) is sitting there in the JSON. That is the only place it's visible; nothing on the Executions list itself flags it.",
      "The actual fix: add an IF node right after the HTTP Request node, checking whether its output contains an error field. Wire the \"true\" branch to a Slack or email node so a real failure sends you an alert instead of vanishing into a green checkmark.",
    ],
    changes: [
      "n8n's \"On Error: Continue\" setting is designed to survive a minor hiccup and keep the rest of the workflow running — that part is a real, useful feature, not a bug.",
      "The gap is what happens next: a node set to Continue that actually fails does not change the workflow's own Success/Error status at all — the Executions list has no visual difference between \"ran perfectly\" and \"this step silently failed.\"",
      "This matches a dated, first-person report from n8n's own community forum (May 2026, independently confirmed by a second user in July 2026): a real production workflow stayed silently broken for weeks because the Executions list never stopped reading Success.",
    ],
    limits: [
      "This is about the \"On Error: Continue\" and \"Continue (using error output)\" settings specifically — a node left on the default \"Stop Workflow\" behaves as expected and does flag the workflow as failed.",
      "The fix shown (an IF node checking for an error field) has to be added to every node you've set to Continue — it isn't a global setting that protects a whole workflow at once.",
      "Verified against n8n's current official docs and community reports as of this episode, not personally re-tested against every n8n version — if n8n changes this behavior in a future release, re-check before relying on this exact setup.",
    ],
  },
  {
    n: 30,
    title: "AI chats love padding the answer before they actually answer you.",
    standfirst:
      "One instruction, pasted once into any AI chat, stops the hedging: it answers " +
      "the question directly first, and only explains further if you ask. Verified " +
      "with a real captured before/after on the same question — before the paste, a " +
      "multi-paragraph breakdown; after, two words. Not a setting change and not tied " +
      "to one AI tool — it works the same in ChatGPT, Claude, or Gemini because it's " +
      "just an instruction the chat follows for the rest of that conversation.",
    steps: [
      "Open any AI chat you already use — ChatGPT, Claude, or Gemini, in a browser or the app.",
      "Ask it something you'd normally ask — any real question with more than a yes/no answer.",
      "Read the answer. Most models open with a paragraph of context or hedging before the actual point.",
      "In the same conversation, paste this exact instruction as its own message: \"Answer first, in one sentence. Then explain, only if I ask. Skip caveats unless they change the answer.\"",
      "Send it. The AI will confirm it understood — that confirmation is not yet a re-answer to your original question.",
      "Ask your original question again, in the same chat. This time the answer opens with the direct point, not a lead-up.",
      "This only holds for the rest of this conversation — a new chat starts fresh, so paste it again at the start of any new conversation where you want the same behavior.",
    ],
    changes: [
      "This is a plain instruction-following behavior, not a hidden setting or a feature exclusive to one AI tool — any capable chat model honors it the same way.",
      "It doesn't make the AI's answers more correct or more complete — it only changes the order and amount of hedging before the actual point arrives.",
      "Verified with a real captured example on the same question, asked twice in the same chat: before the paste, a multi-paragraph answer with headers and a list; after, a two-word direct answer.",
    ],
    limits: [
      "It resets every new conversation — this is not a persistent account setting like ChatGPT's Custom Instructions, so it has to be pasted again in each new chat.",
      "For questions that genuinely need nuance (medical, legal, anything where a caveat actually changes what you should do), the instruction already tells the AI to keep caveats that \"change the answer\" — but always read past the first sentence when the topic actually calls for it.",
      "Not tested identically across every model version — behavior demonstrated on ChatGPT; the underlying mechanism (instruction-following) is standard across current chat models, but exact phrasing sensitivity can vary slightly between them.",
    ],
  },
  {
    n: 31,
    title: "ChatGPT needs the internet to respond. This AI doesn't — and it just proved it.",
    standfirst:
      "A real, working AI model, run entirely on your own machine, with the network " +
      "cut at the system level — not airplane mode, an actual disconnected namespace. " +
      "Asked directly, the model still guesses wrong that it needs the internet, " +
      "because nothing about how it works gives it that information. Free, " +
      "open-source, and it keeps working after the one-time download.",
    steps: [
      "Install Ollama: on Mac or Linux, paste curl -fsSL https://ollama.com/install.sh | sh into a terminal and press Enter. On Windows, use PowerShell and paste irm https://ollama.com/install.ps1 | iex instead.",
      "Once it finishes, download a model with a network connection: type ollama pull llama3.2 and press Enter. This step needs the internet — it's the only one that does.",
      "Optional, to prove it to yourself: turn off WiFi (or unplug ethernet) once the download finishes.",
      "Type ollama run llama3.2 and press Enter. It starts and answers with zero network connection.",
      "Ask it anything — a question, a coding request, a word problem. The answers are real, generated entirely on your machine.",
      "To try a different model instead: ollama pull phi3 (smaller, faster) or ollama pull gemma2 (a middle ground) — swap the model name in both the pull and run commands.",
    ],
    changes: [
      "This is standard, current Ollama behavior — verified live: v0.32.5 as of this episode, free and open-source (MIT license).",
      "Only ollama pull and ollama push need a network connection. Once a model is downloaded, ollama serve and every query after it run with no network at all — confirmed in this episode inside an isolated network namespace with a verified-failed outbound connection.",
      "The model itself has no way to know it's running locally — asked directly whether it's connected to the internet, it answered (wrongly) that it's a cloud-based model that needs one. This isn't a bug specific to one model; language models generally have no built-in way to introspect their own deployment.",
    ],
    limits: [
      "The one-time model download does need real internet — this is an offline-after-setup tool, not a zero-download one.",
      "A modern laptop with 16GB RAM comfortably runs 7-8B parameter models; larger models (Llama 4, some Qwen 3 variants) need considerably more.",
      "Model names move fast — this episode uses llama3.2, the current official quick-start model as of this episode; check ollama.com's model library for the current recommended default before assuming an older name (llama3, phi3) is still the best starting point.",
    ],
  },
  {
    n: 32,
    title: "n8n never tells you when a workflow dies. Almost nobody turns on the fix.",
    standfirst:
      "By default, a failed n8n node just turns red in your execution history — no " +
      "email, no Slack message, nothing. Most people never open that history until " +
      "something already feels wrong, by which point it could have been broken for " +
      "weeks. The fix is one setting: an Error Workflow, wired to an Error Trigger node.",
    steps: [
      "Create a new, separate workflow — this will be your Error Workflow, not one of your regular automations.",
      "Add an Error Trigger node as the first (and only required) node in this new workflow.",
      "Add a notification node after it — a Slack message or Send Email node works well — and reference the Error Trigger's own output fields (workflow name, error message, node that failed) in the message.",
      "Save and activate this Error Workflow.",
      "Open each existing workflow you want protected, go to its Settings (the three-dot menu → Settings), and set 'Error Workflow' to the one you just built.",
      "Test it: deliberately break a duplicate or test workflow (never a production one) and confirm the notification arrives.",
    ],
    changes: [
      "This is standard, current n8n behavior — verified live this session against n8n's own current documentation on error handling.",
      "By default, a failed execution only shows as a red X in the Executions list — there is no notification of any kind unless an Error Workflow is explicitly configured.",
      "n8n ships its own official template for exactly this pattern (\"Attach a default error handler to all active workflows\"), confirming this is a recommended, current, and supported setup — not an improvised workaround.",
    ],
    limits: [
      "The Error Workflow has to be set per-workflow (or applied to all active workflows via n8n's own template) — it is not automatically on for every workflow in an account by default.",
      "This tells you a workflow failed; it doesn't diagnose why on its own — the Error Trigger's output data (the error message, the failing node) is what you use to investigate.",
      "Test on a duplicate or test workflow first — deliberately breaking a production workflow to test this is not worth the risk.",
    ],
  },
  {
    n: 33,
    title: "Your n8n AI agent isn't broken. It's forgetting on purpose.",
    standfirst:
      "The Agent node's memory window defaults to 5 exchanges — nobody sets " +
      "it, it just ships that way. Ask a follow-up question six messages " +
      "later and the agent has no idea what you're talking about. To " +
      "whoever's talking to it, that reads as broken, not smart.",
    steps: [
      "Open the workflow with your AI Agent node and click into its Memory sub-node (Simple Memory, Postgres Chat Memory, or Redis Chat Memory, whichever is wired in).",
      "Find the 'Context Window Length' field — this is the number of past exchanges replayed into the prompt on every message. Confirm it's still the default (5).",
      "Raise it to a number that fits a real conversation — 20 to 50 exchanges covers most customer-facing use cases without over-stuffing the prompt.",
      "If you're running n8n in queue mode, do not use Simple Memory — its context does not follow across workers, so a conversation can silently reset mid-session.",
      "Switch to Postgres Chat Memory or Redis Chat Memory instead — both persist to an external store that survives both restarts and queue-mode worker switches.",
      "Test with a real back-and-forth that crosses your old window size (e.g., ask something, then ask a follow-up 6-10 messages later) to confirm the agent still remembers.",
    ],
    changes: [
      "This is standard, current n8n behavior — verified live this session against current n8n Agent node memory documentation and setup guides.",
      "The context window is a sliding cap on what gets replayed into the prompt, not on what's stored — older messages stay saved per session, they just stop being sent to the model once the window fills.",
      "Simple Memory's per-worker limitation in queue mode is a real, documented gotcha, not an edge case — any queue-mode deployment with Simple Memory is affected.",
    ],
    limits: [
      "A larger context window means a longer, more expensive prompt on every message — there's a real cost/quality tradeoff, not just 'bigger is always better.'",
      "This fixes forgetting within the configured window; it does not give the agent persistent memory across completely separate sessions unless the memory node itself is set up for that.",
      "Postgres/Redis memory requires that datastore to already be reachable from your n8n instance — this is a bigger setup step than Simple Memory's zero-config default.",
    ],
  },
  {
    n: 34,
    title: "That n8n node you built didn't run once. It ran once for every item.",
    standfirst:
      "n8n's real execution model: a node doesn't run once per workflow, it runs once " +
      "per item in the array it receives. That's why an HTTP Request node on 40 rows " +
      "makes 40 real calls, not one call with 40 rows in it — and why a workflow that " +
      "\"ran fine\" on 3 test items can quietly rate-limit or blow through a bill at 300.",
    steps: [
      "Open any node in your workflow and check its input — n8n shows it as a list of items, not one blob of data.",
      "Run the workflow with a small test set (2-3 items) and watch the node execute once per item in the Executions panel — this is normal, not a bug.",
      "Before an expensive or rate-limited step (an HTTP Request to a paid API, for example), add a Loop Over Items node — officially named 'Split in Batches' in n8n's own docs.",
      "Set the batch size on the Loop Over Items node to however many items you want processed together per pass, rather than one at a time.",
      "Wire the expensive node inside the loop, and any per-batch waiting (a Wait node, for a rate limit) inside the same loop.",
      "Test again with a larger set (dozens of items) to confirm the batching actually slows the expensive step down the way you intended.",
    ],
    changes: [
      "This is standard, current n8n behavior — verified live this session against current n8n documentation and community threads on per-item execution.",
      "The Loop Over Items node's current official name is 'Loop Over Items (Split in Batches)' per n8n's own docs (updated June 2026) — 'Split in Batches' alone is its older/internal name.",
      "Per-item execution is the core of n8n's data model, not an edge case — every node in every workflow works this way, whether or not a Loop node is present.",
    ],
    limits: [
      "This explains and manages per-item execution; it doesn't remove real per-call cost or rate limits — batching controls the pace, it doesn't make the calls free.",
      "Batch size is a real tradeoff: too large risks hitting a rate limit anyway, too small barely helps — the right number depends on the specific API's own limits.",
      "Test with a set close to your real production volume before trusting a workflow at scale — 3 test items behaving fine says nothing about 300.",
    ],
  },
  {
    n: 35,
    title: "Your n8n automation can say \"done\" — and still do it twice.",
    standfirst:
      "n8n's Webhook node, on its default setting, waits until the whole automation " +
      "finishes before replying back. If that takes more than a few seconds, whatever " +
      "sent the original event has no way to know it's still being handled — so it " +
      "sends the exact same event again, and n8n runs the entire automation a second " +
      "time, real actions included.",
    steps: [
      "Open your workflow's Webhook (trigger) node and check its 'Respond' setting — if it says 'When Last Node Finishes', the reply is held until every node in the workflow completes.",
      "Time a real run in the Executions panel. If it regularly takes more than a few seconds, whatever calls this webhook may already be timing out and retrying on its own.",
      "Change the Webhook node's 'Respond' setting to 'Using \\'Respond to Webhook\\' Node'.",
      "Add a 'Respond to Webhook' node immediately after the trigger, before any real work (sending an email, creating an order, calling another API) — this sends the reply the instant the event arrives.",
      "Move every node that does real, side-effect-causing work to run AFTER the Respond to Webhook node, not before it.",
      "Re-run a real test and confirm in the Executions panel that the response fires immediately, while the rest of the workflow still completes normally afterward.",
      "(Optional) If the sender still shows retry attempts in its own logs, add simple de-duplication (checking an incoming ID against a short-lived store) as a second layer, not a replacement for responding fast.",
    ],
    changes: [
      "This is standard, current n8n behavior — verified live this session against n8n's own Webhook and Respond to Webhook node docs and a live Community forum thread describing this exact failure mode.",
      "n8n Cloud also hard-cuts an unanswered webhook at 100 seconds (a 524 response) — moving the reply earlier avoids that limit entirely, it isn't just about the caller's own timeout.",
      "This is a different failure than a node's own retry setting replaying one step (see episode 25) — here the TRIGGER fires the whole workflow again from outside, because nothing told it the first attempt was received.",
    ],
    limits: [
      "This stops duplicate runs caused by a slow reply; it does not protect against a sender that retries for a different reason (e.g. its own network error) — de-duplication is the real fix for that, not response timing alone.",
      "Moving the reply earlier means the caller can no longer see the workflow's own output in that response — if the caller genuinely needs the result synchronously, this tradeoff needs a different design (e.g. polling a status endpoint).",
      "This does not undo damage from duplicate runs that already happened — check for and clean up any real double-sends before assuming the fix alone is enough.",
    ],
  },
  {
    n: 36,
    title: "ChatGPT trains itself on everything you've ever typed to it.",
    standfirst:
      "That's turned on by default for Free, Plus and Pro accounts — and it's not just " +
      "chat history. The files you upload and the answers you get back become " +
      "training data too, unless you turn one setting off.",
    steps: [
      "Open ChatGPT on the web or the app, and open Settings (click your name/profile in the bottom-left on web, or the profile icon in the app).",
      "Go to the 'Data Controls' section of Settings.",
      "Find the toggle labeled 'Improve the model for everyone' — if it's on (the default for Free/Plus/Pro accounts), your conversations, uploaded files and the answers you receive are being used to train future models.",
      "Switch that toggle off.",
      "Understand what this does and doesn't do: every conversation you have AFTER turning it off stays out of training completely. It does NOT retroactively remove anything already sent before you turned it off — once a conversation entered the training pipeline, this toggle can't pull it back out.",
      "(Optional, for a single sensitive conversation) Instead of relying on the toggle, start a 'Temporary Chat' (the toggle/icon near the message box, or a dedicated button depending on your app version) — it never enters your chat history and is never used for training, automatically, every time, with nothing to remember to turn off.",
      "Confirm the change stuck: open a new regular chat afterward and check Settings → Data Controls again — the toggle should still read off.",
    ],
    changes: [
      "Verified live (16.9.2026) against OpenAI's own Help Center articles: 'How your data is used to improve model performance' and 'What if I want to keep my history on but disable model training?' — this is current, documented behavior, not assumed from an older version of ChatGPT.",
      "Default state confirmed as ON for Free/Plus/Pro accounts, and OFF by default for Temporary Chats and Business plans, per the same source.",
      "This is a plain-language, personal-privacy topic — a deliberate exception to this channel's usual demand-report-driven topic selection, made explicitly per the 16.9.2026 reach-first content decision (see channel/content-memory.md).",
    ],
    limits: [
      "Turning the toggle off is not retroactive — anything sent before you turned it off may already be part of a training run and cannot be pulled back out by this setting.",
      "Temporary Chat still stores the conversation on OpenAI's servers for up to 30 days for safety monitoring before permanent deletion — it skips history and training, not all server-side storage.",
      "This episode covers OpenAI's ChatGPT specifically; other AI tools (Claude, Gemini, etc.) have their own separate data-training settings, not covered here.",
    ],
  },
  {
    n: 37,
    title: "Google's AI has already looked at every photo you've ever taken.",
    standfirst:
      "Ask Photos (powered by Gemini) can already answer questions like \"find the best " +
      "shot from every trip I've taken\" — which means it already analyzed every photo " +
      "in your library, not just the ones you search for. One setting controls whether " +
      "people can review the questions you ask it.",
    steps: [
      "Open the Google Photos app on your phone (or photos.google.com on the web).",
      "Tap your profile picture in the top-right corner, then tap 'Photos settings' (on web: Settings via the gear icon).",
      "Look for the Ask Photos / 'Ask Photos' section (may also appear under a general 'AI features' or 'Gemini' heading, depending on your app version and region).",
      "Find the toggle for allowing your questions to be reviewed by people to improve the feature — wording varies by version, but it's the one governing human review of your Ask Photos queries.",
      "Switch it off if you don't want your questions reviewed by anyone besides the automated system.",
      "Understand what this does and doesn't do: this controls who can review the QUESTIONS you type into Ask Photos. It does not stop the AI from having already analyzed the content of your photo library — that's the feature working as designed, on by default.",
    ],
    changes: [
      "Verified live (17.9.2026) against Google's own Ask Photos support page and independent 2026 coverage of the feature's rollout and its privacy-toggle mechanic.",
      "A plain-language, personal-privacy topic — a deliberate exception to this channel's usual demand-report-driven topic selection, made explicitly per the 16.9.2026 reach-first content decision (see channel/content-memory.md), same reasoning as episode 36.",
    ],
    limits: [
      "The exact toggle wording and menu path can vary by app version, region, and account type (personal vs. Workspace) — this guide describes what to look for, not a guaranteed identical screen for every viewer.",
      "Turning off human review of your queries does not delete or undo the AI's existing analysis of your photo library — there is currently no publicly documented Google Photos setting that reverses that.",
      "This episode covers Google Photos' Ask Photos specifically, not Google's broader AI/Gemini data policies across its other products.",
    ],
  },
  {
    n: 38,
    title: "Ten seconds of your voice is all AI needs to clone it now.",
    standfirst:
      "Scammers only need a few seconds of your real voice — from a public video, a social " +
      "post, or a voicemail greeting — to clone it with current AI tools, then call someone " +
      "you love pretending to be you, asking for money. The real defense isn't a setting in " +
      "an app: it's a shared safe word only your loved ones know.",
    steps: [
      "Get the people who'd ever need to reach you in an emergency together — in person, or a group chat everyone's already in. This doesn't work if only one person knows it.",
      "Agree on two random, unrelated words nobody could guess or find online — not a pet's name, not a birthday, not an inside joke you've ever posted. Example: a made-up pairing like 'lighthouse-pretzel'.",
      "Say the words out loud together once, so everyone has actually heard them spoken, not just read them in a text.",
      "Save it somewhere each person can find later without asking out loud in the moment — a private note on your phone, not just memory.",
      "Agree on the rule: if anyone calls sounding distressed and asking for money, gift cards, or crypto, the other person asks for the safe word before doing anything else.",
      "Agree on the fallback: if the caller can't give it, hang up and call that person back on the number already saved in your phone — never the number that just called, since caller ID can be faked.",
      "Test it once, on purpose, in a calm moment — not during a real scare — so everyone actually knows the drill when it matters.",
    ],
    changes: [
      "Verified live (17.9.2026) against multiple independent 2026 cybersecurity/consumer-safety and voice-cloning-industry sources, cross-referenced rather than relying on a single outlet: current instant-cloning APIs (e.g. Gradium, Cartesia) specify a 10-second minimum sample; the caller-ID-spoofing mechanic and the safe-word defense are also current and consistent across sources.",
      "A plain-language, personal-safety topic — a deliberate exception to this channel's usual demand-report-driven topic selection, made explicitly per the 16.9.2026 reach-first content decision (see channel/content-memory.md), same reasoning as episodes 36 and 37.",
    ],
    limits: [
      "A safe word stops the specific 'fake emergency call' scam pattern described here — it doesn't protect against every kind of scam or fraud.",
      "This only works if it's actually agreed upon in advance and everyone involved remembers it exists — it protects nothing if only one person set it up.",
      "This episode covers the voice-cloning phone-scam pattern specifically, not broader AI-deepfake risks (video, images) which use different mechanisms and defenses.",
    ],
  },
  {
    n: 39,
    title: "Your smart TV is watching what you watch.",
    standfirst:
      "Most smart TVs run Automatic Content Recognition (ACR) by default: the TV " +
      "periodically fingerprints what's on screen — from any device plugged into it, not " +
      "just its own apps — and sends that back to build an ad profile. A real, per-brand " +
      "setting turns it off.",
    steps: [
      "Samsung: open Settings, go to 'Device Preferences' (or 'General' on some models), then 'Usage & Diagnostics', and turn off the data-reporting toggles there — this disables Samsung's ACR/Samba integration.",
      "LG: open Settings (the gear icon), find 'Live Plus' (LG's ACR feature) and switch it off; nearby, also turn on 'Limit Ad Tracking' to reduce ad profiling further.",
      "Vizio: open the TV's menu, go to 'System' then 'Reset & Admin', and turn 'Viewing Data' off — this disables Vizio's ACR and viewing logs.",
      "Roku (built into many TVs and Roku streaming devices): from the Roku home screen, go to Settings, then 'Privacy', and turn off 'Personalize ads' — this stops interest-based ad tracking tied to your device.",
      "Don't have one of these exact brands? Look in your TV's settings for anything named 'Viewing Data', 'ACR', 'Live Plus', 'Interest-Based Ads', or 'Usage & Diagnostics' — the feature exists under a different name on most smart TVs.",
      "Understand what this does and doesn't do: turning this off stops the TV from reporting what's on your screen going forward. It doesn't delete data already collected, and it doesn't turn off ads themselves — only the profile-building behind them.",
    ],
    changes: [
      "Verified live (17.9.2026) against multiple independent 2026 consumer-tech and cybersecurity sources, cross-referenced: how ACR works, its typical check-in frequency (Samsung roughly once a minute, LG roughly every 15 seconds), and the real per-brand opt-out menu paths.",
      "Backed by active, current 2026 legal action confirming this is a live issue, not stale: Texas's Attorney General sued Samsung, Sony, LG, Hisense, and TCL over ACR data collection (Samsung settled February 2026); Kentucky passed the first state law requiring opt-in consent for ACR in March 2026.",
      "A plain-language, personal-privacy topic — a deliberate exception to this channel's usual demand-report-driven topic selection, made explicitly per the 16.9.2026 reach-first content decision (see channel/content-memory.md), same reasoning as episodes 36-38.",
    ],
    limits: [
      "Exact menu wording and location can vary by TV model year and firmware version — this guide describes what to look for, not a guaranteed identical screen for every viewer.",
      "Turning ACR off does not delete data already collected and reported before you changed the setting.",
      "This episode covers ACR specifically, not other data a smart TV or its apps may collect (account data, app usage inside a streaming app, voice assistant recordings), which have their own separate settings.",
    ],
  },
  {
    n: 40,
    title: "Do you know who's already grading how you drive?",
    standfirst:
      "Most new cars have built-in tech that tracks your speed, braking, and location " +
      "automatically. Automakers have sold that data to companies that build reports " +
      "insurers use to help set your rate — California settled with GM for $12.75 million " +
      "over exactly this in May 2026. A real setting turns off the sharing, and you have a " +
      "free legal right to see what's already been collected on you.",
    steps: [
      "Open your car's own mobile app (e.g. myGM/OnStar, FordPass, Toyota app, or your manufacturer's equivalent) and sign in.",
      "Look in the app's Settings or Privacy section for something named 'Connected Services', 'Data Sharing', 'Smart Driver', or 'Driving Data' — wording varies by brand.",
      "Turn off any toggle that shares your driving behavior or location data with third parties — this is usually separate from turning off safety features like crash notification, which you likely want to keep.",
      "If you can't find it in the app, check your car's own touchscreen settings menu for a similar 'Connected Services' or 'Data Privacy' section — some brands only expose it there.",
      "Request your own free consumer disclosure report from LexisNexis Risk Solutions: go to consumer.risk.lexisnexis.com and submit a request (needs your name, address, and date of birth), or call 1-800-456-6004. This is a real, federal right (FCRA) — the same law that lets you request a free credit report — and it shows you what's actually been collected under your name.",
      "Understand what this does and doesn't do: turning off the sharing setting stops new data from being sent going forward. It does not delete or undo data already shared with brokers or insurers before you changed it.",
    ],
    changes: [
      "Verified live (17.9.2026) against multiple independent 2026 auto-industry, insurance-trade, and privacy sources, cross-referenced: California's Attorney General's $12.75M settlement with GM (May 2026, over selling OnStar Smart Driver data to LexisNexis and Verisk); that as of March 2026 GM stopped that specific data-sharing pipeline; and that the broader industry practice (91% of new US cars have telematics, multiple manufacturers still share with brokers) continues.",
      "LexisNexis's own consumer disclosure process (free report request under federal law) verified directly against LexisNexis's own site (consumer.risk.lexisnexis.com).",
      "A plain-language, personal-stakes topic — a deliberate exception to this channel's usual demand-report-driven topic selection, made explicitly per the 16.9.2026 reach-first content decision (see channel/content-memory.md), same reasoning as episodes 36-39.",
    ],
    limits: [
      "Exact app menu wording and location vary by car manufacturer and model year — this guide describes what to look for, not a guaranteed identical screen for every viewer.",
      "The GM-to-LexisNexis/Verisk pipeline specifically was already shut down by GM as of March 2026 — this guide is about the ongoing, broader industry practice at other manufacturers, and about your standing right to check your own file regardless of which company held it.",
      "Verisk's current, active involvement in collecting driving data is unclear in available sources — this guide treats LexisNexis as the primary, confirmed contact for a consumer disclosure request.",
    ],
  },
  {
    n: 41,
    title: "ChatGPT can now see every subscription draining your bank account",
    standfirst:
      "ChatGPT has a real feature called Finances: connect your actual bank accounts, cards, " +
      "and investments through Plaid, and it lays out your spending, every recurring " +
      "subscription, and what's coming up — all in one dashboard. It's read-only: it can't " +
      "move money, pay anything, or place a trade.",
    steps: [
      "In ChatGPT, open 'Finances' from the left sidebar and select 'Get started' — or type '@Finances, connect my accounts' in any conversation.",
      "Follow the secure Plaid flow to log into your bank, card, or brokerage account (12,000+ institutions supported, including Chase, Amex, Schwab, Fidelity, Robinhood, and Capital One).",
      "Wait a few minutes while ChatGPT syncs and categorizes your accounts, then open the Finances dashboard to see spending, subscriptions, upcoming payments, and portfolio performance.",
      "Look specifically at the subscriptions view — it consolidates every recurring charge across your connected accounts in one place, including ones you may have forgotten you're paying for.",
      "To disconnect at any time: go to Settings → Apps → Finances and remove the connection. OpenAI states your synced data is deleted from ChatGPT within 30 days.",
      "You can also view and delete ChatGPT's saved financial 'memories' directly from the Finances page, separately from disconnecting the account link itself.",
    ],
    changes: [
      "Verified live (17.9.2026) directly against OpenAI's own product announcement (openai.com/index/personal-finance-chatgpt) plus independent press (TechCrunch, MacRumors, gHacks), cross-referenced: what the Finances dashboard shows, that it's explicitly read-only (can't move money, pay bills, or place trades), and the exact enable/disconnect steps.",
      "A real, current, named ChatGPT feature at the center of the claim — not a generic tech/privacy angle — per the 17.9.2026 standing rule added to channel/hooks-guide.md after episodes 39-40 drifted toward weak or zero AI relevance while chasing reach.",
      "A plain-language, personal-stakes topic under the 16.9.2026 reach-first content decision (see channel/content-memory.md), same reasoning as episodes 36-40.",
    ],
    limits: [
      "As of this recording, Finances is live for ChatGPT Plus and Pro subscribers in the United States only — not the Free tier, and not yet available globally.",
      "It launched as a Pro-only US preview on 15.5.2026 and was reported to expand to Plus users by around 25.6.2026 — availability by plan may keep changing as OpenAI continues the rollout.",
      "It cannot move money, pay bills, or place trades — it only reads and displays data from accounts you've connected; it does not replace a budgeting app that can act on your behalf.",
    ],
  },
  {
    n: 42,
    title: "Your phone might already have an AI that can catch a scammer mid-call",
    standfirst:
      "Google's Phone app has a real feature called Scam Detection: an on-device AI model " +
      "(Gemini Nano) that listens to a live call for the patterns scammers use — urgency, " +
      "gift cards, someone claiming to be your bank — and alerts you mid-call if it's " +
      "suspicious. It's fully on-device and private. It's off by default.",
    steps: [
      "Make sure your Phone app is updated to the latest version.",
      "Open the Phone app, tap 'More', then 'Settings', then 'Scam Detection'.",
      "Turn on 'Scam Detection'.",
      "During a live call, if the risk is high, you'll get a notification, sound, and vibration — an audible beep also plays at the start of the call and periodically through it.",
      "You can dismiss a false alarm by selecting 'Not a scam', or end a suspicious call immediately.",
      "To turn it off for one call only: tap 'More' then 'Scam Detection' during that call. To turn it off for all calls: Phone app → More → Settings → Scam Detection → toggle off.",
    ],
    changes: [
      "Verified live (18.9.2026) directly against Google's own support documentation (support.google.com/phoneapp/answer/15654065) plus independent press (Android Police, Tom's Guide, Bleeping Computer), cross-referenced: exactly what the feature listens for, that it's fully on-device ('No conversation audio or transcription is stored on the device, sent to Google servers or anywhere else'), and the exact on/off steps.",
      "A real, current, named AI model (Gemini Nano) at the center of the claim — per the 17.9.2026 standing rule added to channel/hooks-guide.md, and deliberately a different company/product from episode 41's ChatGPT topic per David's direct note to vary which AI product gets featured.",
      "A plain-language, personal-stakes topic under the 16.9.2026 reach-first content decision (see channel/content-memory.md), same reasoning as episodes 36-41 — anchored to a real, dated stake (FTC: $2.95B in reported 2024 impersonation-scam losses).",
    ],
    limits: [
      "Pixel-only, and only specific models: in the US, Pixel 6 and later plus Pixel 9a/10a; internationally (Australia, Canada, France, Germany, India, Ireland, Italy, Japan, Mexico, Singapore, Spain, UK), Pixel 9 and later, with a SIM and device location in one of those countries.",
      "This is a different feature from Google's separate spoofed-caller-ID detection (which works across Samsung/OnePlus but only flags number spoofing, not conversation content) — this guide covers Scam Detection specifically.",
      "It's off by default — it does nothing until you turn it on in Settings.",
    ],
  },
  {
    n: 43,
    title: "Windows is already screenshotting your whole screen",
    standfirst:
      "Windows 11 has a real feature called Recall: an AI model that saves a screenshot of " +
      "your screen every few seconds and turns the whole history into something you can " +
      "search, in plain language. It's off by default and locked behind Windows Hello — but " +
      "a published tool can already walk past that lock.",
    steps: [
      "Open Settings (Win+I), then go to 'Privacy & security'.",
      "Select 'Recall & snapshots'.",
      "Check the toggle next to 'Save snapshots' — if it's off, Recall is already off and saving nothing; skip the rest of these steps.",
      "If it's on: select 'Open Recall' (or search 'Recall' in the Start menu) to see and search the history it's already saved.",
      "To turn it off completely: on the same 'Recall & snapshots' page, turn the 'Save snapshots' toggle off, then select 'Delete all snapshots' to remove anything already stored.",
      "Optional — to keep Recall on but limit what it sees: on the same page, open 'Filter app content' and turn off snapshots for specific apps (e.g. banking, password managers) individually.",
    ],
    changes: [
      "Verified live (20.9.2026) directly against Microsoft's own Learn/Support documentation plus independent press (Computerworld, XDA Developers, the maintained Wikipedia timeline), cross-referenced: that Recall is opt-in and off by default (a real correction from its original 2024 opt-out design, stated as the current state, not the old one), the Windows Hello + 'proof of presence' lock, and the exact settings path.",
      "A real, current, named AI feature (Recall) at the literal center of the claim — per the 17.9.2026 standing rule added to channel/hooks-guide.md — and a third distinct company from episodes 41 (OpenAI/ChatGPT) and 42 (Google/Android), per David's direct note to vary which company gets featured.",
      "A plain-language, personal-stakes topic under the 16.9.2026 reach-first content decision (see channel/content-memory.md): a searchable record of everything you've ever done on your PC needs no technical background to feel the stake.",
      "The bypass tool named in the hook and script (TotalRecall Reloaded, published 9.4.2026 by security researcher Alexander Hagenah) is a real, dated, named incident — not a hypothetical risk — stated plainly rather than smoothed over.",
    ],
    limits: [
      "Recall requires a Copilot+ PC (specific NPU-equipped hardware) and a supported Windows 11 build — it is not available on every Windows PC, even if the toggle exists in Settings on some machines it will do nothing without the right hardware.",
      "Turning the setting off does not undo whatever a bypass tool may have already copied before you turned it off — this setup only controls whether Recall keeps saving snapshots going forward, and lets you delete what it's already stored.",
      "This guide is Windows/Recall only — it does not cover any other AI feature's own screen-recording or activity-history behavior on macOS, ChromeOS, or other platforms.",
    ],
  },
  {
    n: 44,
    title: "AI can already read your private messages",
    standfirst:
      "WhatsApp has a real feature called Message Summaries: Meta AI reads your unread " +
      "messages in a chat and gives you a bulleted summary, so you can catch up without " +
      "reading everything yourself. It's off by default, and Meta says its own AI never " +
      "sees your real messages while generating the summary.",
    steps: [
      "Make sure WhatsApp is updated to the latest version.",
      "Open WhatsApp, go to Settings, then 'Chats', then 'Private Processing'.",
      "Turn on 'Private Processing features'.",
      "Open any chat with unread messages, and tap the '(Number) unread messages' divider.",
      "Select 'Summarize privately' to see a bulleted summary of what you missed.",
      "To turn it off: go back to Settings → Chats → Private Processing and turn the toggle off.",
    ],
    changes: [
      "Verified live (20.9.2026) directly against WhatsApp's own blog (blog.whatsapp.com) and Help Center (faq.whatsapp.com) plus independent press (TechCrunch, 9to5Mac, GSMArena), cross-referenced: what Message Summaries does, the exact settings path, and Meta's own 'Private Processing' privacy claim, stated here as Meta's claim rather than an independently confirmed fact.",
      "A real, current, named AI feature (Message Summaries, built on Meta AI) at the literal center of the claim — per the 17.9.2026 standing rule added to channel/hooks-guide.md — and a fourth distinct company from episodes 41 (OpenAI/ChatGPT), 42 (Google/Android) and 43 (Microsoft/Windows), per David's direct note to vary which company gets featured.",
      "A plain-language, personal-stakes topic under the 16.9.2026 reach-first content decision (see channel/content-memory.md): an AI reading the content of your private messages needs no technical background to feel the stake.",
    ],
    limits: [
      "Rollout is limited to select markets, starting with the US in English — Meta states it is expanding to more countries and languages, with no fixed date given.",
      "Meta's own materials acknowledge a generated summary 'might be inappropriate or inaccurate' — treat it as a starting point, not a substitute for reading anything you need to act on.",
      "This guide covers Message Summaries specifically, not any other Meta AI feature inside WhatsApp, Instagram, or Facebook.",
    ],
  },
];

export const articleFor = (n: number) => ARTICLES.find((a) => a.n === n) ?? null;
export const promptFor = (a: Article | null) =>
  a?.promptSlug ? PROMPTS.find((p) => p.slug === a.promptSlug) ?? null : null;
