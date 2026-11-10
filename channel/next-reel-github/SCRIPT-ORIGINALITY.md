# Script originality check, next reel (8.11.2026)

David: the s2 script was "basically the same" as @jesserurka "Part 2: Vibe Coding Essentials". He was right. This file compares old s2, the reference, and the new script (s3).

## What was too close (s2 vs the reference)
- Same beat order: answer first -> identity line "nobody shows you" -> save/commit -> GitHub online -> push -> clone -> branch -> merge -> "tell your AI to ...".
- Same phrasings: "go back to the one that worked" (ref: "go back to the last commit that worked"), "Nobody shows you this when AI builds your app" (ref: "nobody showed you"), "say this to your AI: save this version" (ref: "tell Claude to commit and push").
- Same metaphor: a timeline of save points (the ref's "timeline"), plus a game-save analogy.

## What s3 does instead
| | s2 (old) | s3 (new) |
|---|---|---|
| Order | crash -> sentence -> why -> nobody shows you -> game save -> git/GitHub -> push -> clone -> branch/merge -> say this to AI | hook -> OUR bad edit breaks the app -> one command brings the file back -> WHY it works (Git takes pictures) -> photo album -> GitHub copy online -> push survives a lost laptop -> the loop to copy |
| Metaphor | timeline + save point + game boss | photo album: each commit is one picture. Git's own book says "Git basically takes a picture of what all your files look like at that moment" (git-scm.com/book, What is Git?), so it is accurate |
| Dropped | -- | "nobody shows you", the game, clone, branch, merge, any AI-sentence ending, the Tomorrow line |
| Ending | "So say this to your AI: save this version." | "Ahead of each AI edit, take a picture. That's git commit." + "Working? Commit. Broken? Undo it. Repeat." and a card with the two real commands |
| Middle | same real run | same real run (terminal-output.txt, git 2.43.0) and the real GitHub screenshots of 7.11.2026; the break is labelled A BAD EDIT |

## New script (spoken)
1. GitHub is the undo button for AI apps.
2. One bad edit, and my tip app prints NaN.
3. I typed one command. The working file came back.
4. It works because Git takes a picture of your files.
5. Each commit is one picture. Your project becomes a photo album.
6. GitHub keeps a second copy of that album online.
7. Push once, and a lost laptop can't take your history.
8. Ahead of each AI edit, take a picture. That's git commit.
9. Working? Commit. Broken? Undo it. Repeat.

## Shared words with the reference (honest list)
Only the unavoidable product words: GitHub, Git, commit, push, laptop (the ref says laptop in a 3D render). No shared sentence, no shared order, no timeline/save-point metaphor. The one remaining structural similarity: the middle is a real use case (a break, then the fix), which is the point of our own tested artifact.

## Claims checked (live, 8.11.2026)
- "Git takes a picture of your files" / commit = snapshot: git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F, quoted: "every time you commit, or save the state of your project, Git basically takes a picture of what all your files look like at that moment".
- `git restore app.js` returns the file to the last snapshot: git-scm.com/docs/git-restore (default source is the index, which equals the last commit when nothing is staged, as in our run). True only for edits that were not committed; for a committed bad edit our run used `git revert` (shown in terminal-output.txt, not in this cut).
- "GitHub keeps a second copy online" and "a lost laptop can't take your history" are true only after a push: line 7 says "Push once".
- "Working? Commit. Broken? Undo it." is a shortened loop, true for uncommitted breaks. The card says `git restore app.js`.
- Not verified here: GitHub docs page on commit history returned 404 on the URL tried; the commits screenshot itself is the real page of 7.11.2026.
