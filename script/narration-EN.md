# Universal AI Engine — Narration Script (English)

**Runtime target:** ~14:00 (timecodes below are editor targets; ±10% is fine)
**Voice direction:** Calm, confident, warm. Pace ~160 wpm including pauses. Not hypey.
Pause 0.5s at every `//`. Words in **bold** get a light emphasis lift.
**Audience:** A non-technical ChatGPT user. Assume they know nothing about AI beyond "I type, it answers."

> Terminology rule for the whole video: never say "prompt engineering", "system prompt",
> "token", "inference" or "context window" without immediately explaining it in plain words.

---

## S1 — HOOK · 00:00–00:30

Most people use ChatGPT like a search box. // They type a question, they get an answer, and it's… fine.

But here's the thing. ChatGPT already knows dozens of ways to think. It can compare. It can argue against itself. It can find risks you didn't ask about. It can break a problem down to first principles.

It just doesn't do any of that — **unless you ask.**

In the next thirteen minutes I'm going to show you a single block of text you paste into ChatGPT **one time**. After that, ChatGPT decides on its own which of those thinking methods your question needs. //

No shortcuts. No slash commands. No memorising anything. You just talk normally — and the answers get sharper.

Let's build it.

---

## S2 — WHAT THIS ACTUALLY IS · 00:30–01:35

First, let's be honest about what we're building, because there's a lot of nonsense online.

We are **not** installing software. We are **not** buying a new AI. We are **not** unlocking a hidden mode.

What we're doing is called a **Custom Instruction**. Think of it like this. //

Imagine you hire a brilliant assistant. Genuinely brilliant — knows everything. But on day one, they have no idea how *you* like to work. So every single morning you'd have to repeat: "when I ask you something big, think it through properly, show me the risks, tell me what you're assuming."

Exhausting, right?

A Custom Instruction is a note you pin to that assistant's desk. **Once.** They read it before every conversation, forever.

That's it. That's the whole trick. We are writing one very good note. //

I call this particular note the **Universal AI Engine** — because instead of giving ChatGPT one instruction, we're giving it a menu of about forty ways of thinking, plus the judgement to pick the right ones by itself.

---

## S3 — SHORTCUTS VS. AUTOMATIC · 01:35–02:50

Now, you may have seen the popular version of this idea online. It usually looks like this. //

Someone gives you a list of commands. Slash-deep. Slash-godmode. Slash-critic. Slash-simplify. And the deal is: if you remember to type the magic word, you get a better answer.

I want you to notice the problem with that. // **You** have to remember. **You** have to know which method your question needs. Which means you have to already understand deep reasoning, red-teaming, first-principles thinking, and second-order effects — just to pick the right shortcut.

That's backwards. You came here for help thinking. Now you need expertise just to *ask* for help thinking.

So this system flips it. //

Instead of "here are the commands you can type", we tell ChatGPT: *here is everything you know how to do — you choose.*

You type: "should I build this app?" — in completely normal words. And ChatGPT works out on its own that this question deserves assumptions, risks, alternatives and a recommendation.

Same question. No shortcut. Much better answer. // That's the entire difference.

---

## S4 — HOW IT ACTUALLY WORKS · 02:50–04:05

Let me show you what's happening underneath, in plain language.

Every time you send a message, ChatGPT doesn't just read your message. It reads three things stacked on top of each other. //

**Layer one** — OpenAI's own rules. Safety, behaviour, the basics. You can't touch that, and you don't want to.

**Layer two** — **your** Custom Instructions. This is the layer we're editing today. It's your standing orders. It gets read **before** your message, every single time, in every new chat.

**Layer three** — the message you just typed.

So when you write "should I build this app?", ChatGPT is really seeing: *"Reminder: you are a Universal AI Engine, here are forty thinking methods, pick the useful ones, challenge assumptions, name risks, end with a decision."* — and **then** your question. //

Your question hasn't changed. The **instructions wrapped around it** have.

And that's why this feels like a different AI. It isn't. It's the same model, finally being told what good work looks like. //

One more thing, and this is important for later: our instruction includes a **recipe for hard questions**. Understand — break it down — state assumptions — challenge them — look at alternatives — find risks — improve — decide — give one next step.

Nine steps. ChatGPT runs them quietly, in the background, and hands you the finished thinking. Not the mess.

---

## S5 — WHERE TO INSTALL IT · 04:05–05:05

Okay. Let's find the right screen. This is the part people get wrong, so go slowly with me.

We are **not** typing this into a chat. If you paste it into a normal conversation, it only works in that one conversation, and it's gone tomorrow. //

We want it in **Settings**, so it applies everywhere, forever.

Here's the path. Open ChatGPT — the website or the app, either is fine. //

Look for your **profile picture or your initials**. On desktop it's usually bottom-left or top-right. On mobile, tap the menu, then your name at the bottom.

Click it, and choose **Settings**.

Then find **Personalization**. //

Inside Personalization you're looking for **Custom instructions**. Tap it.

Now — one honest note. OpenAI redesigns this screen fairly often. The words might be slightly different by the time you watch this. // It may say "Personalization", it may say "Customize ChatGPT". Don't panic. **You are looking for the screen with the empty boxes that ask what ChatGPT should know about you.** That's always the right place.

---

## S6 — THE EXACT SETUP · 05:05–06:40

You'll see a few boxes. Typically: a nickname, what you do for work, what traits ChatGPT should have, and a bigger one for anything else.

Here's what matters. //

The box you want is the **large free-text one** — usually the last one, labelled something like **"Anything else ChatGPT should know?"**, or on some versions, the traits box.

Honestly? If you're unsure — the big empty box is the right box. Both feed the same layer.

Now paste the instruction. It's on screen, and it's in the description below the video, so you never need to type it by hand. //

Let's read the key parts as it goes in, so you actually understand what you're installing.

Line one: *"You are my Universal AI Engine."* — that sets the role.

Then: *"Automatically choose the best methods for every request. I should not need to use shortcuts."* — that's the whole point of the system, stated up front.

Then the long list — writing, simplifying, first principles, Feynman, analogies, SWOT, steelman, red team, second-order effects, Pareto, systems thinking, and about thirty more. This is the menu. //

Then the guardrail — and this one matters more than people think: *"Select only what is useful. Do not overthink simple requests."*

Without that line, you ask "what's the capital of France" and get a four-page strategic analysis. // With it, simple questions stay simple.

Then the nine-step recipe for complex decisions. Then the writing rule. Then the honesty rule — *never invent facts, separate facts from assumptions*. And finally the language rule, which tells it to answer in your language — even if you type that language using English letters.

Now — the two things people forget. //

**One:** make sure the toggle is **on**. Depending on your version it says "Enable for new chats" or similar. If that's off, none of this runs.

**Two:** press **Save**. Not back. Not escape. **Save.** // If you navigate away without saving, you've done nothing.

---

## S7 — TESTING THAT IT WORKED · 06:40–07:30

Now let's prove it's live. Two rules first. //

Rule one: **open a brand new chat.** Old conversations that were already running may not pick this up. New chat. Always.

Rule two: don't test it with something trivial.

Here's the test I use. In a fresh chat, type — normally, no shortcuts:

*"Should I quit my job to work on my side project full time?"* //

Watch what comes back. You're looking for four fingerprints. //

**One** — it names the assumptions it's making, instead of pretending to know your situation.
**Two** — it gives you the case for *and* the case against.
**Three** — it raises risks you did not ask about.
**Four** — it ends with an actual recommendation and a concrete next step. Not "it depends on you".

If you see those four things, it's working. //

If you see a flat, generic, five-bullet answer with no assumptions and no recommendation — go back to Settings. Nine times out of ten, the toggle is off, or you never hit Save.

---

## S8 — EXAMPLE 1: EVALUATING AN APP IDEA · 07:30–08:45

Let's watch it work on real questions. Three examples. Watch what I type — because I'm going to type like a normal human being.

Example one. I type: //

*"I want to build an app that reminds people to drink water. Is it a good idea?"*

That's it. Eleven words. No commands, no formatting, no magic.

Now watch what comes back. //

It doesn't just say yes or no. First it separates **what it knows** from **what it's assuming** — it flags that it doesn't know my budget, my audience, or whether I can build it myself.

Then it does something I never asked for: it **compares** my idea to what already exists — and points out that phones already have reminders built in, and that this category is extremely crowded.

Then **risks**. Retention. People delete these apps in a week. That's the killer, and I didn't ask about it. //

Then it **reframes** — it suggests the real opportunity might not be reminders at all, but a narrow group with a medical reason to track intake.

And then it **decides**. A recommendation, and one next step: talk to ten people in that group before writing a line of code. //

Now — notice what it did *not* do. It never said "I'm now applying comparison, then risk analysis, then decision-making." It just… thought properly. That's deliberate. The last line of our instruction says the goal is the best answer, **not showing off the method.**

---

## S9 — EXAMPLE 2: SAAS OR MOBILE APP · 08:45–10:00

Example two. A real decision with real trade-offs. I type: //

*"Should I build a SaaS or a mobile app?"*

Nine words. Deliberately vague — because that's how people actually ask.

Watch the shape of the answer. //

First it does the thing almost nobody does: it says the question **can't be answered as asked**, and tells you exactly which three facts would change the answer. Who's paying. Whether it needs to work offline. And whether you're selling to businesses or to individuals.

But — and this is the key — it does **not** stop and interrogate you. // It states its assumptions out loud and answers anyway. That's the difference between a useful advisor and an annoying one.

Then a genuine **comparison**. Cost to build. Time to first paying customer. App-store approval — which can take days and can reject you. Ongoing maintenance across two phone platforms instead of one website.

Then the **second-order effects** — the consequences of the consequences. Choose mobile, and you've signed up for app-store fees and update cycles for years. // That's not a launch problem, it's a three-year problem. Most people don't think that far.

Then a **clear recommendation**, with the exact condition that would flip it: *"go SaaS — unless your product genuinely needs the camera, GPS, or push notifications."*

That last part is what makes it usable. It doesn't just decide. It tells you **when to change your mind.**

---

## S10 — EXAMPLE 3: EXPLAINING AN AI AGENT · 10:00–11:00

Third example — and this one shows the system going the *other* way.

I type: //

*"What is an AI Agent?"*

Now, remember the rule: don't overthink simple requests. This is a knowledge question. There's no decision to make, no risk to weigh. So a good engine should **not** run the nine-step decision process here. And it doesn't. //

Instead it switches into teaching mode. Watch. //

It starts with the plainest possible sentence: a normal chatbot answers you. An **agent** actually goes and does things — several steps, in order, using tools, until the job is done.

Then an **analogy** — that's the Feynman method, explaining like you're five. A chatbot is a colleague who answers your question. An agent is a colleague who takes the task, disappears, and comes back when it's finished. //

Then a concrete **example**. "Find me a flight" versus "book me a flight, compare four sites, pick the cheapest with legroom, and put it in my calendar."

Then the honest **limitation** — agents break in ways chatbots don't, because one wrong step early ruins every step after it.

And it ends by checking your understanding. //

Same instruction block. Completely different behaviour. Because the engine read the question and picked teaching, analogies and examples — instead of risks and decisions. That is the whole promise of this system, working.

---

## S11 — BEST PRACTICES · 11:00–11:55

Four things that make this dramatically better. //

**One — write like you talk.** Don't try to write clever prompts anymore. The instruction is doing that job now. Messy, honest, human questions actually work best, because the more context you give it, the better it reasons.

**Two — always start a new chat for a new topic.** The instruction loads at the start. Don't drag a two-week-old conversation into a new decision. //

**Three — you can still override it.** The instruction is a default, not a cage. If it goes too deep, just say "shorter". If it goes too shallow, say "challenge that harder". It obeys the message in front of it over the standing note.

**Four — add two lines about yourself.** Your job, your language, what you're working on. Because "should I build this app?" is a completely different question for a student and for someone with a team of ten. // Give it that, and the quality jumps immediately.

---

## S12 — LIMITATIONS · 11:55–12:55

Now the part most tutorials skip. Let's be straight with each other. //

**This is not a new AI model.** It's the same ChatGPT. You have not upgraded anything. You've given better instructions.

**This is not software.** Nothing was installed. There's no app, no plugin, no account. It's text in a settings box.

**It doesn't make ChatGPT correct.** It makes it think more carefully — and a careful thinker can still be confidently wrong. Our instruction tells it never to invent facts and to separate facts from assumptions, and that genuinely helps. It does not make it a guarantee. **Check anything that matters.** //

And here's the most important distinction in this whole video. //

Custom Instructions are **guaranteed to be delivered.** That part is mechanical — OpenAI reliably puts your text in front of the model, in every new chat. That's the part you can count on.

Whether the model **follows** every line, every time — that's not a guarantee. That's a language model doing its best to comply. // It'll follow the spirit almost always, and occasionally drift on a specific rule.

So: delivery, guaranteed. Obedience, very likely. Not certain. Anyone telling you otherwise is selling something. //

Last one: it applies to **new chats**, not old ones. And if you use ChatGPT on your phone and your laptop, it follows your account — so it's already on both.

---

## S13 — RECAP · 12:55–13:40

Let's put it together. //

You opened Settings, went to Personalization, opened Custom instructions, pasted one block of text, made sure the toggle was on, and pressed Save.

That's the entire installation. Maybe ninety seconds of work. //

And from now on, in every new chat, ChatGPT reads a note that says: *here are forty ways of thinking — you work out which ones this question deserves.*

You don't type shortcuts. You don't memorise commands. You ask like a human. //

The instruction is in the description. Paste it, change the language line to your own language, and go and ask it something you're genuinely stuck on.

That's where you'll feel the difference. // See you in the next one.
