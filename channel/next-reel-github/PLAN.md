# Next reel after episode 86: "Git/GitHub, the undo button for AI-built apps" (7.11.2026)
Labels: FACT = read or run today; HYPOTHESIS = my reading; UNKNOWN = not obtainable. Scores are my judgement, not measurements. Nothing in the repo was edited, nothing published.
Files here: PLAN.md, script-A.txt / script-B.txt / script-C.txt, timings.txt (estimated), lint/lint-*.txt (script_lint, all 0 risky words), demo/run-demo.sh + demo/terminal-output.txt (real run), logos/ (GitHub Invertocat SVG, official logo zip, Claude svg from ep86).

## 1. Topic decision
DECISION: same subject as the reference (what Git and GitHub are, for people who build with AI), but our angle is "the undo button": the problem shown live, then the sentence to say to the AI. Not a close sibling.
Why (data):
- FACT (demand-report.md): "claude code tutorial beginners" median 159,426 views, "ai agents explained" 124,549, n8n 233,070. The measured demand is for building with AI, not for everyday-phone tips. This topic sits in that audience, which is also the audience that buys the paid service (the "sell" finding). Git/GitHub itself is NOT in the demand report: UNKNOWN demand for this exact keyword. Claude Code is the closest measured proxy.
- FACT (content-memory.md, CONFIRMED 21.9): a mechanism the viewer can act on at once saves better than a pure reveal. "Say this sentence to your AI" is exactly that.
- FACT (ref-reel analysis): the reference shows the beat order works for 132K plays; HYPOTHESIS: format vs the 37-42K account is not separable. David accepted that risk.
- Not covered before: grep of channel/ and the episode scripts found no Git/GitHub episode. FACT: Claude Code appears in ep 23/25 era only as a tool, never this angle.
- Honest risk (HYPOTHESIS): our channel's recent packaging rule (6.10, "an everyday thing happening to the viewer's phone") does not fit a developer topic. We keep the reference's identity gap instead ("nobody showed you"). Audience = people who make apps with AI, narrower than our ep 80/72 audience. Expect a different reach profile; log it as an experiment.
What is COPY (from the reference): the subject, the plain-question hook (candidate A), the beat order (answer, identity line, live problem, one-sentence fix, 3-4 s micro-beats push/clone/branch/merge, closing sentence to say to the AI + follow reason), always-moving picture, no wipes.
What is OURS: the tested artifact (a real git run, verbatim output), a game "save point" metaphor instead of a timeline, the "go back to the last version that worked" fix shown with real command output, light + lime base, our drawn UI (no "Habits" app, no 1972 claim, no 96.65% survey, no profile card), real logos, our voice, the tomorrow line.

## 2. Verified facts (checked live 7.11.2026)
FACT, GitHub docs (docs.github.com/en/get-started/start-your-journey/about-github-and-git): "Git is a version control system that tracks changes to files." "GitHub is a platform for building software." GitHub hosts Git projects (repositories) in the cloud. Git helps you "merge your work with other people's changes safely".
FACT, GitHub docs "About Git": file history appears "as snapshots in time called commits"; "`git commit` saves the snapshot to the project history"; commits are organised into "multiple lines of development called branches"; "`git merge` merges lines of development together"; "`git push` updates the remote repository with any commits made locally to a branch"; "`git clone` creates a local copy of a project that already exists remotely".
FACT, GitHub docs "Creating a new repository": plus icon top right ("Create something new") > "New repository" > name > visibility public/private > optional README > "Create repository". The page is undated, so UI labels are UNVERIFIED against today's live site (I could not open a logged-in github.com). Do not show a pixel-exact GitHub screen; draw it, or capture the real page by hand first.
FACT, Claude Code docs (code.claude.com/docs/en/checkpointing): Claude Code tracks its own file edits; `/rewind` (or Esc twice on an empty prompt) opens a menu with "Restore code and conversation", "Restore conversation", "Restore code"; limits: changes made only by Bash commands are not tracked ("use version control, such as Git"); subagent edits often not restored; snapshots deleted about 30 days after the session; "Not a replacement for version control ... continue using version control, such as Git". This is the honest "why Git when Claude has rewind" answer, and a possible one-line caveat on /e/N.
FACT, our own run (git 2.43.0, node v22.22.0, 7.11.2026): demo/terminal-output.txt. Commands that work as shown: git init -b main, add, commit, status, diff, log --oneline, restore, revert --no-edit, remote add, push -u, clone, switch -c, merge, tag, push --tags, pull.
FACT: GitHub brand page (brand.github.com/foundations/logo): official zip https://brand.github.com/GitHub_Logos.zip (downloaded, has SVG/PNG Invertocat black/white and "GitHub_Lockup" files). Rules: logos in articles about GitHub are permitted; modifying (colours, dimensions, combining with other words) is prohibited; the Invertocat alone is meant for "GitHub-owned environments or where the brand is already clearly established". CONSEQUENCE: on frame 0 use the unmodified official wordmark lockup (GitHub_Lockup_Black.svg) rather than the bare mark, never recolour it, never put our own words inside the badge. Claude logo: use the same claude.svg ep86 already uses (source of that file not re-verified today: UNKNOWN, check against Anthropic's brand page before reuse).
UNVERIFIED / not claimed: that Git is "free" (not checked, do not say it); the year Git began (not needed, not said); that GitHub is "where everyone" keeps code; the exact current wording a Claude Code session shows when it commits (not run: no Claude Code in this sandbox); how often AI breaks apps (no data, so scripts say "one day", never a rate). "Will break your app one day" (C) is a prediction, not a statistic: soften to "can break" if David prefers strictly literal.
Caveat that must stay true on screen: `git restore` throws away UNSAVED edits for good. It only brings back what was committed. That is the whole point of "save first", and it is why the demo order is commit, then edit, then break, then restore.

## 3. Our own tested artifact (demo/run-demo.sh, real output in demo/terminal-output.txt)
Tiny tip calculator (`node app.js 80`). Real sequence:
1. commit "Tip calculator works". `node app.js 80` -> `Bill 80 -> tip 12.00, total 92.00`
2. An AI-STYLE edit ("also split the bill") uses `people.count` on a number -> `Each pays NaN`. `git status --short` -> ` M app.js`; `git diff` shows the 3 changed lines.
3. `git restore app.js` -> `node app.js 80` -> `Bill 80 -> tip 12.00, total 92.00` again.
4. Second case, bad edit COMMITTED ("AI: round the tip", `... tip 12, total 95`): `git revert --no-edit HEAD` -> `tip 12.45, total 95.45`; log shows the revert as a new commit, history kept.
5. Local bare folder as the remote: `git push -u origin main`, `git clone remote.git friend-copy`, `git switch -c split-bill`, commit, `git switch main`, `git merge split-bill` (Fast-forward), `git tag v1.0`, `git push origin main --tags` (* [new tag] v1.0 -> v1.0), `git pull` in the first copy, `git tag` -> v1.0.
REAL: every command and its output, verbatim. DRAWN: the phone/app window and the GitHub website screen (nothing on github.com was driven), the "AI" typing. NOT REAL (say it, or fix it before shipping): the bad edit was written by me, to imitate a typical AI mistake; no Claude Code or ChatGPT run produced it. The script must not claim "Claude broke it" unless David records a real Claude Code edit that breaks the app (about 5 minutes on his machine; Claude Code in this sandbox is not available). Best option: he records that real break, we keep the real git output for the rest.

## 4. Three candidates (spoken lines in script-*.txt; timings in timings.txt are ESTIMATES at 3.0 words/s plus pauses, ASSUMPTION; real voice may run 10-20% longer)
Voice rule: all lines linted, 0 risky words. Lines are short; no word the voice swallows ("computer"/"before"/"remember" swapped out). Final line = tomorrow line (CLAUDE.md rule) naming #2; binding promise. Open conflict to flag to David: rubric B (E1/F2) prefers no spoken outro after the value; CLAUDE.md final-line rule and the reference both end with a follow reason. Ep 86 dropped the spoken outro (David 5.11). Candidates keep the tomorrow line as the last sentence; deleting it saves 6 s and a risk of drop-off. David decides. The "setup's in the link in bio" line is omitted on purpose; the copy-paste setup (steps to install git, make a GitHub account, the two sentences to say) goes in `studio/lib/articles.ts` /e/N, English labels only, as the setup-guide gate requires.

### Candidate A "What is GitHub?" (closest copy of the reference) - 133 words, est. 48 s (over the 45 s ceiling, trim lines 8-10 if needed)
1 What is GitHub? And why does everyone who builds with AI keep saying it?
2 It keeps your app, and every version it ever had.
3 The tool inside is Git. It tracks every change.
4 If you learned to build with AI, nobody showed you this.
5 Watch. One bad edit, and the app is dead.
6 Tell your AI: go back to the last version that worked.
7 Fixed. That version is a commit. A save point, like in a game.
8 Push sends it to GitHub.   9 Clone copies it to a new laptop.
10 A branch is a side copy, for risky tries. Merge brings it back.
11 Now say this to your AI: save this version, and push it to GitHub.
12 Tomorrow, I'll show you why AI says to hide a secret key. Follow for the full story.
Identity line ("nobody showed you") is a claim about the viewer, true only for people who learned by prompting; the hook says "builds with AI" so it addresses exactly them. HYPOTHESIS, copied from the reference, not tested by us.
STORYBOARD (sound-off test: the pictures alone must say "this tool lets you undo a broken app"):
- 0.0-4.8 Frame 0 already moving: the official GitHub lockup (top, inside safe area y 269+) lands on a light card with a drawn app window; a lime ring and a big question mark pulse; caption (top, 1-4 words, key word lit lime): "What is GitHub?". The app window is alive (a tiny bar chart animating) so the first frame is the "healthy app".
- 4.8-8.3 The app window peels into a stack of 5 thin copies behind it, each labelled v1..v5 (drawn): "every version" is visible. Caption "Every version".
- 8.3-11.8 A small Git icon is NOT used (we have no verified logo; do not invent); instead a text chip "Git" in plain type under the GitHub lockup with a thin arrow "GitHub keeps what Git tracks". Caption "Git tracks changes".
- 11.8-15.7 Identity beat: a drawn phone with a chat bubble "Build me an app" (generic AI chat, no brand needed, or the real ChatGPT/Claude logos on two chips), the app appears, then a faded question mark and caption "Nobody showed you this". Slow gentle zoom (no pop).
- 15.7-19.1 PROOF: the real terminal output, typed at natural speed: `$ node app.js 80` / `Each pays NaN` in red, the app window cracks (drawn) and goes grey. Caption "One bad edit".
- 19.1-23.0 A chat bubble (AI) typed: "go back to the last version that worked" (the exact words lit as spoken). Terminal: `$ git restore app.js` then `$ node app.js 80` -> `Bill 80 -> tip 12.00, total 92.00` in green; the app window turns healthy again. This is the payoff, at about 40% of runtime (rubric C1 asks about 30%: weaker than B/C).
- 23.0-27.9 `git log --oneline` real line `ab0955b Tip calculator works` is circled; the circle becomes a game-style save icon (drawn floppy/flag) with caption "Commit = save point".
- 27.9-37.1 Four 2.5-3 s micro-beats on one drawn timeline of save-point dots: dots go up to a cloud shaped GitHub lockup (push), a second laptop drawn receives them (clone), a side line forks off and rejoins (branch, merge). Each beat has one label word only.
- 37.1-42.0 Closing card: the two sentences as copyable text "save this version" / "push it to GitHub", the words lit as said (screenshot-able save card).
- 42.0-48.1 Tomorrow line over a drawn key icon turning into a lock; no new info. Hard cut to frame 0 (loop).

### Candidate B "This app just died" (result-first, then the answer) - 118 words, est. 43 s - RECOMMENDED
1 This app just died. One sentence brought it back.
2 The sentence: go back to the last version that worked.
3 It only works if a save point exists. GitHub is where those live.
4 Nobody shows you this when AI builds your app.
5 In a game, you save ahead of the boss. In an app, that save is a commit.
6 Git makes the save. GitHub keeps a copy online.
7 Push sends your saves there.   8 Clone gets them on a new laptop.
9 A branch is a side copy, for risky tries. Merge brings it back.
10 So say this to your AI: save this version.
11 Tomorrow, I'll show you why AI says to hide a secret key. Follow for the full story.
Differences from the reference: it opens on the problem + result, not the question; the answer (GitHub) comes in line 3. Honest accuracy: "GitHub is where those live" is loose; save points live in Git on your machine, GitHub holds a copy. Line 6 fixes that within 10 s; if David wants zero looseness change line 3 to "GitHub keeps a copy of those."
STORYBOARD:
- 0.0-3.4 Frame 0: split picture. Left half: the drawn app window, grey, cracked, a red `Each pays NaN` line (REAL string). Right half: the same app healthy, green, with `total 92.00`. A lime arrow loops from left to right with the sentence start typed in the middle; official GitHub lockup top; caption top "One sentence". Moving: the crack spreads, the arrow draws itself.
- 3.4-7.0 The sentence fills the screen word by word as spoken: "go back to the last version that worked" (lit lime on each word). Beneath it the real command `git restore app.js` types.
- 7.0-11.7 A drawn game-style save icon pulses on a dot labelled "Tip calculator works" (the real commit message) with real `ab0955b`; the GitHub lockup appears behind it as a cloud. Caption "Save point".
- 11.7-15.0 Identity: a prompt "Build me an app" being typed into a chat (generic), the app pops up, a drawn question mark over a blank "save" button. Caption "Nobody shows you this". (Keep it 3 s, no extra words.)
- 15.0-21.0 Metaphor beat: a drawn game screen, a hero near a boss, a save icon appears; it morphs into the real log line `ab0955b Tip calculator works`. Caption "Commit = save".
- 21.0-24.4 Two chips slide in: "Git" (plain type, makes the dot) and the GitHub lockup (copy online).
- 24.4-33.7 Four micro-beats on the same timeline of dots: push (dots fly up to the GitHub cloud), clone (a second drawn laptop fills with the same dots), branch (a side line forks), merge (it rejoins; the real `Fast-forward` line flashes small). 2.5 s each, one label.
- 33.7-36.9 Save card: "save this version" in big type with a drawn copy-able chip, lit as said.
- 36.9-43.0 Tomorrow line with the drawn key/lock; last frame cuts straight to frame 0.
Real vs drawn: terminal lines are real output; app window and cloud are drawn.

### Candidate C "Do this first" (direct address, practical order: save BEFORE the break) - 126 words, est. 46 s
1 Your AI will break your app one day. Do this now.
2 Say: save this version. That makes a save point, called a commit.
3 Git makes the save. GitHub keeps a copy online.
4 Nobody shows you this when AI builds for you.
5 Now one bad edit. The app is dead.
6 Say: go back to the last save that worked. It lives again.
7 Want a copy if your laptop dies? Say: push it to GitHub.
8 Want to test a wild idea? Say: make a branch. That is a side copy.
9 Like it? Say: merge it back.
10 Two sentences to keep: save this version. Go back to the last one that worked.
11 Tomorrow, I'll show you why AI says to hide a secret key. Follow for the full story.
Truth note: "will break your app one day" is a prediction. Also, commits created by saying "save this version" assume the AI tool can run git (Claude Code does; chat-only AI tools cannot): UNVERIFIED for the exact sentence in every tool, so the caption must say "works in a coding agent that can run commands, such as Claude Code". Not tested here.
STORYBOARD: 0-4.1 frame 0 shows a calm app window with a slowly forming crack and the official GitHub lockup; caption top "Your AI will break it". 4.1-8.5 the chat bubble "save this version" types, a save dot with the real commit line appears ("Tip calculator works"). 8.5-11.9 Git chip + GitHub lockup. 11.9-15.1 identity beat as in B. 15.1-18.2 real terminal `Each pays NaN`, app greys. 18.2-22.6 bubble "go back to the last save that worked", real `git restore` and green output, app heals (payoff at about 40-48% of runtime). 22.6-34.5 three 3-4 s beats with a speech bubble each ("push it to GitHub": dots to cloud and a second device; "make a branch": fork; "merge it back": rejoin), real push/merge lines flash. 34.5-39.9 save card with the two sentences, lit as said. 39.9-46 tomorrow line, key/lock, hard cut to frame 0.
Sound-off check: all three tell the same visual story (healthy, cracked, healed, dots going to a cloud and a second device). Every moving item carries meaning: crack = break, arrow/heal = restore, dots = save points, cloud = GitHub copy, fork = branch. No decorative particles.
Layout rules: nothing in top 14% / bottom 35% / 6% sides except the watermark; captions at top inside the safe box (reference style: 1-4 words, key word lit); no handle on full-bleed screens; no black wipes (dips or crossfades only); light + lime base; typed text at slightly varying speed; no sloppy easing.

## 5. Pre-publish scores (my judgement against B-rubric.md and the 4.11 concept gate; NOT measurements, no promise of views)
Rubric B: H1 frame 0 shows subject with real logo, moving: A PASS (but frame 0 is a question, subject is a logo + healthy app), B PASS, C PASS. H2 subject+stake in first 4 words: A FAIL ("What is GitHub?" has subject, no stake), B PASS ("This app just died"), C PASS (but product is AI, GitHub only on frame). H3 mute test: all PASS if the caption text is large. H4 one specific question answered, answer real: A PASS (answered 8-23 s), B PASS ("which sentence" answered at 3-7 s), C PASS. H5 13-year-old/8-year-old: A borderline ("builds with AI", "version"), B ok, C ok; "commit", "branch", "merge" are explained in the same breath, "Git" is introduced with its job. H6 no invented numbers: all PASS (no numbers, only the demo's own values). C1 payoff by about 8 s: A FAIL (23 s, 48%), B PASS (3-7 s), C FAIL (22 s, 48%; the fix comes after the setup). C3 real and shown: all PASS for the git output, with the "bad edit is simulated" caveat unless David records a real AI break. E1 no outro after value: all FAIL by design (tomorrow line) unless David drops it. E2 loop: PASS (hard cut). E3 no comment bait: PASS. S1 named person: all WEAK/FAIL honestly ("send to a friend who builds with AI", "your friend who vibe codes"): add it in the caption, not the voice. S2 keepable artifact in reel and caption: PASS (two-sentence card + caption). D1 not majority text: PASS if the real frame is mostly drawn picture. D2 safe area: to check with safe_check.js, not run (nothing built).
Numeric (CLAUDE.md gate: hook >= 90 / virality >= 85):
- A: hook 80, virality 74. Reasons: long question, no felt stake (-10), fix at 48% (-5), identity line only partly "you" (-3), loop and save card good (+). Closest to reference, weakest by our own rules. To raise: cut to "What is GitHub? Nobody showed you." ... still under 85.
- B: hook 91, virality 83. Reasons for hook: product + stake in 9 words, specific gap (which sentence), visible in frame 0, plain words. Virality: personal and felt (4/6 of the concept checklist: specific thing, gap, saveable card, 30-s checkable claim), named person weak (point 4: caption only), watch-twice detail (the loop and a small `ab0955b` hash that returns) is real but small. Below 85 by 2: to lift, record a REAL Claude Code break on David's machine (point 1 becomes real and "happening to the viewer's own tool"), and add the on-screen "send to the friend who builds with AI" chip during the save card.
- C: hook 90, virality 82. "You" in titles measured x0.88 within channels (viral-hook-lab prior, correlational), the prediction wording is a hypothesis; payoff late (48%); strongest on practical order and saveable card. 
None reaches 95 honestly. Under the 85 virality gate, B plus the two changes above is the only one that can reach 85. HYPOTHESIS: the numbers have no calibration against our own views (ep 85 will start it). Log predicted score and real 48 h views in content-memory.md.

## 6. Series plan and caption
Series name (ours, not the reference's "Vibe Coding Essentials"): "AI Builder Basics" (working title; check it is free before use, UNKNOWN).
- #1 "The undo button for apps AI builds" (Git and GitHub).
- #2 "Why AI tells you to hide a secret key" (API keys, .env files, what a leak costs). Must be verified live before the tomorrow line is recorded; promise is binding.
- #3 "What 'deploy' means: how your app gets a link anyone can open".
Caption (3 lines, Instagram accepts '>' but we avoid it; English):
Say these two sentences to your AI: "save this version" and "go back to the last version that worked."
Git keeps the saves, GitHub keeps a copy online. Full steps: actually-works.com/e/N (setup in plain clicks).
Send this to the friend who builds apps with AI. #2 tomorrow: why AI says to hide a secret key. Follow for the series.
Experiment log entry (channel/experiments.md, to add when built): "Copy of reference structure (@jesserurka Part 2) on our own tested git run. Test: result-first hook B vs question hook A. Read 48 h: views, 2 s/5 s skip, sends, saves, follows. Account-size confound stays unseparable."
Build notes: GitHub lockup unmodified from the official zip; our run is the only terminal text; the drawn "app window" is a generic tip calculator, no brand copied from the reference; no "1972", no survey.

## 12-line summary
1 Topic: Git and GitHub as the undo button for AI-built apps (same subject as the reference, our angle).
2 Copy: subject, hook shape, beat order, always-moving picture, closing sentence to say to the AI. Ours: real git run, save-point metaphor, light + lime base, our voice, the tomorrow line.
3 Facts verified live today: GitHub docs (Git, GitHub, commit, branch, merge, push, clone), Claude Code /rewind limits, GitHub brand rules. Not verified: GitHub UI labels today, Git "free", a real Claude Code run, Claude logo provenance.
4 Artifact: demo/run-demo.sh run today, real output in demo/terminal-output.txt (commit, break to NaN, restore, revert, push, clone, branch, merge, tag).
5 Honest flag: the bad edit was written by me, not by an AI. Do not say "Claude broke it" unless David records a real break; best fix: one real Claude Code recording.
6 Three candidates, all linted clean (0 risky words): A 133 words question hook, B 118 words result-first, C 126 words "do this first".
7 Scores (judgement): A hook 80 / virality 74; B 91 / 83; C 90 / 82. None reaches 95; only B can reach 85 with a real AI break and a "send to" chip.
8 Payoff timing: B delivers at 3-7 s, A and C at about 48% of runtime.
9 Conflict for David: rubric says no spoken outro, CLAUDE.md and the reference end with a follow reason; I kept the tomorrow line, one sentence, droppable.
10 Series: #2 why AI says to hide a secret key; #3 what deploy means. #2 must be verified before the promise is recorded.
11 Branding: use the official unmodified GitHub lockup on frame 0, not the bare Invertocat (brand rules).
12 RECOMMENDATION: build B first; if David insists on the closest copy, build A's body with B's hook as an A/B pair (same body, two hooks) and read both at 48 h.
