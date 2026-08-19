# Screen Recording Guide — exact shot list

Everything the editor needs to capture, in capture order. Record all of it in one
session so the UI theme and window size stay identical across cuts.

## Capture settings

| Setting | Value |
|---|---|
| Resolution | 2560×1440 (gives room to punch in to 130% without softness at 1080p) |
| Frame rate | 60 fps capture, conform to 30 fps (smoother cursor, cleaner slow-mo) |
| Browser zoom | 100%, window maximised, bookmarks bar hidden |
| Theme | Pick dark **or** light and never mix. Dark reads better against the video's palette |
| Cursor | Record real cursor; enlarge and add glow in post, not with an OS accessibility setting |
| Typing | Type at a natural ~55 wpm. Do not paste text you're pretending to type |
| Streaming answers | Capture the real streaming response — do not fake it. If it's too slow, speed-ramp in post to 2–4× and drop a `sped up` chip |

## Privacy pass (do this before recording, not after)

- Log into a clean account or a fresh profile with no personal chat history.
- If the sidebar shows real conversation titles: blur them in post at 20px Gaussian, or collapse the sidebar entirely.
- Hide the account email in the settings menu (blur in post — a black box looks amateur).
- Turn off notifications and any browser extensions that render badges.

## Shot list

### BLOCK A — the "wrong place" shot (S5)
- **A1** Open a normal chat. Paste the full instruction into the **message box**. Do not send. Hold 3s.
  *Post: red ✗ and "Not here."*

### BLOCK B — navigation (S5)
- **B1** From a chat screen, move cursor slowly to the **profile picture / initials**. Pause 1s before clicking. Click.
- **B2** Menu open. Pause 1s. Click **Settings**.
- **B3** Settings modal open. Pause 1s. Click **Personalization**.
- **B4** Click **Custom instructions**. Let the panel fully open. Hold 3s.
- **B5** Repeat B1–B4 **on mobile** (screen-record the iOS/Android app: menu → your name at the bottom → Settings → Personalization → Custom instructions). Used as a picture-in-picture inset.

> If your build shows **Customize ChatGPT** instead of **Personalization**, record that path too and cut both as the two thumbnails in S5's honesty card.

### BLOCK C — filling it in (S6)
- **C1** Empty Custom instructions panel, all fields visible. Hold 4s — this is the frame the labels animate onto.
- **C2** Click into the **large free-text field** (usually the last one — *"Anything else ChatGPT should know?"*). Hold 1s.
- **C3** Paste the full instruction. Let the field scroll. Hold 3s at the end.
- **C4** Slow-scroll the field from top to bottom over ~8s so the editor can sync the block-by-block highlights.
- **C5** Cursor to the **Enable for new chats** toggle (or equivalent). Toggle it OFF then ON, deliberately, so post can ring it.
- **C6** Cursor to **Save**. Pause 1s. Click. Capture the success state / panel closing. Hold 3s.

### BLOCK D — the test (S7)
- **D1** Click **New chat**.
- **D2** Type live: `Should I quit my job to work on my side project full time?` Send.
- **D3** Capture the full streaming answer, uncut, to the end. Then scroll slowly top→bottom over ~10s so post can dock the checklist ticks.

### BLOCK E — example 1 (S8)
- **E1** New chat. Type live: `I want to build an app that reminds people to drink water. Is it a good idea?` Send.
- **E2** Full streaming capture, then a slow scroll pass.

### BLOCK F — example 2 (S9)
- **F1** New chat. Type live: `Should I build a SaaS or a mobile app?` Send.
- **F2** Full streaming capture, then a slow scroll pass.

### BLOCK G — example 3 (S10)
- **G1** New chat. Type live: `What is an AI Agent?` Send.
- **G2** Full streaming capture, then a slow scroll pass.

### BLOCK H — best practices (S11)
- **H1** In an existing answer thread, type `shorter` → capture the contracted answer.
- **H2** Then type `challenge that harder` → capture the expanded answer.
- **H3** New chat: ask `Should I build this app?` with no context → capture answer.
- **H4** New chat: ask the same with `I'm a student, working solo, no budget.` → capture answer. These two are the side-by-side in S11 ④.

### BLOCK I — the "before" shot (S1)
- **I1** **Record this with Custom Instructions turned OFF**, in a separate browser profile or before you set anything up. Ask `how do I grow my business?` and capture the plain, generic answer.
- **I2** After setup, ask the identical question in a new chat and capture the improved answer. These are the BEFORE/AFTER in the hook.

> **Do BLOCK I-1 first, before you configure anything.** Once the instruction is saved you cannot easily get a clean "before" shot again without disabling it.

## Honesty rules for the recordings

- Every answer shown must be a **real, unedited response** to the question shown. Speed-ramping and trimming for length are fine; rewriting the model's words is not.
- If you trim mid-answer, put a small `trimmed` chip on screen.
- If a take produces a weak answer, re-roll the question rather than editing the text. Show what the system actually does.
