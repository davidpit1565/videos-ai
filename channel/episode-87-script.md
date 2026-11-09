# Episode 87 script (written 9.11.2026): "GitHub is the undo button / Ctrl+Z for AI mistakes"

Topic: what Git and GitHub do for someone who builds apps with AI. Angle: one bad edit breaks a tiny app, one command brings the working file back, then why that works (Git takes pictures) and what GitHub adds (an online copy). Reference-structure check is in `channel/next-reel-github/SCRIPT-ORIGINALITY.md`.

## Spoken lines (line 1 not decided yet; lines 2-9 as in SCRIPT-ORIGINALITY.md)
1. EITHER "AI broke your app? GitHub undoes it." OR "You know Ctrl+Z. GitHub is Ctrl+Z for AI mistakes."
2. One bad edit, and my tip app prints NaN.   (video/nextreel-git/lines-d.txt has "One bad edit, and my tip app is broken." instead: pick one, both are true)
3. I typed one command. The working file came back.
4. It works because Git takes a picture of your files.
5. Each commit is one picture. Your project becomes a photo album.
6. GitHub keeps a second copy of that album online.
7. Push once, and a lost laptop can't take your history.
8. Ahead of each AI edit, take a picture. That's git commit.
9. Working? Commit. Broken? Undo it. Repeat.
No tomorrow line is written here. If the cut ends on line 9 (as in the plan), the caption says "next", not "tomorrow", like episode 86. If a tomorrow line is added, the promise is binding (CLAUDE.md).

## Ground truth
- Real run: `channel/next-reel-github/terminal-output.txt`, 7.11.2026, git 2.43.0, node v22.22.0, local folder `tipcalc`.
  - commit "Tip calculator works"; `node app.js 80` printed `Bill 80 -> tip 12.00, total 92.00`.
  - Edit #1 (NOT committed), labelled A BAD EDIT in the video: `node app.js 80` printed `Each pays NaN` (it reads `people.count` on a number).
  - `git status --short` showed ` M app.js`; `git diff` showed the three changed lines; `git restore app.js` brought back `Bill 80 -> tip 12.00, total 92.00`.
  - Second case (not in the reel cut): a bad edit that WAS committed was undone with `git revert --no-edit HEAD`; history was kept as a new commit.
  - Push/clone/branch/merge were run against a local bare folder standing in for GitHub, not against github.com.
- Real GitHub screenshots of 7.11.2026 (commits and repository pages).
- The bad edit was written by us on purpose to imitate a typical AI mistake. No AI tool produced it.

## Docs read live on 9.11.2026 (see the list in the hand-off and in /e/87)
git-scm.com book (What is Git, Undoing Things, Recording Changes, Working with Remotes, First-Time Setup), git-scm.com/docs (git-restore, git-revert, git-checkout), git-scm.com/install pages, docs.github.com (About GitHub and Git, Quickstart for repositories, Adding locally hosted code to GitHub, About remote repositories, Caching your credentials, Creating an account, Pushing commits to a remote repository), nodejs.org/en/download.

## What is NOT claimed
- That an AI broke the app. The break was our own scripted edit.
- That `git restore` brings back anything committed or deleted for good. It only brings back the file as it was in the last commit or staging area; edits not yet committed are lost when you run it (git book: "a dangerous command").
- That GitHub performs the undo. Git, on your computer, does. GitHub keeps an online copy. Line 1 option A ("GitHub undoes it") and the title are shorthand: the caption and /e/87 say which tool does what.
- That "a lost laptop can't take your history" is true before a push. Line 7 says "Push once".
- That "Working? Commit. Broken? Undo it." covers every break: it is the uncommitted case; after a commit the way back is `git revert` (verified in the docs and in our run).
- That Ctrl+Z works the same way (line 1 option B is a comparison, not a claim of equality: Ctrl+Z undoes steps in one program, Git undoes to a saved picture).
- That this is a rate or statistic of AI breaking apps. No number is claimed.
- One run, one local folder, git 2.43.0 (current Git is 2.56.0 per git-scm.com; the commands used are long-standing and are in the current docs, but we did not re-run them on 2.56.0).

## Hook
Type: identity plus stakes, with a familiar comparison on option B (Ctrl+Z). Hook-type rotation vs episode 86 (curiosity gap plus identity): option A is a problem-and-fix claim, option B is an analogy; both differ, but B is closer to identity. Both state subject (GitHub, AI mistakes) in the first words. Blind-reader check: pending. 72-hour readings: pending.

## Scores (judgements, not measurements; calibration in channel/score-calibration.md)
HOOK: pending
VIRALITY: pending
OVERALL: pending
PREDICTED VIEWS: pending
Concept checklist (4.11 gate): pending
Blind reader answer (first frame plus first second): pending

## Disclosures
Anthropic makes Claude, and this video was made with help from Claude. GitHub is owned by Microsoft; this channel is not affiliated with GitHub or Git. Logos used under their brand guidelines (see SCRIPT-ORIGINALITY.md, brand.github.com).
