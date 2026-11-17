# Episode 104 plan: Agency Agents (Q2, reference reel DfVPw9LTJEo, @auraguy.ai), written 17.11.2026
Publish mode: REGULAR (David, 17.11.2026: no trial until we know why the last videos underperformed). Status: PLAN, not built. Waiting for David's go.
Numbering: 103 = Replica (built, not merged). Internal build folder will be `video/ep105` (ep104 folder is the Replica build).

## TOPIC verdict
Why a stranger cares today: "a free pack of 280 AI specialists for Claude Code" has money (free), a named brand (Claude Code, GitHub) and a big checkable number (169.0k stars, read on GitHub 17.11.2026). It is the strongest of the three reels of that creator (3,992 likes, 1,735 comments; views not exposed). Risk: the audience leans developer, and the reel overclaims ("run your whole business", "AI employees"). We keep the structure and energy, and we say "specialists", not "employees who work 24/7".
Duplicate check 17.11: no hit for agency / agents / specialists in `topics-covered.txt`; the 5 read-only `aw-*` agents we use are not an episode.

## Reference, line by line (Whisper, 69.4 s) and what is on screen
| s | spoken | picture |
|---|---|---|
| 0-4.4 | You can now run your whole business with Claude code for absolutely free. | isometric 3D crowd of tiny figures around an orange pixel-Claude block, "ON TASK" status pill top, white headline bar |
| 4.4-10.5 | You get 280 AI employees who work 24-7 to scale your business and make more money without hiring a single person. | crowd ring, then a 24 h clock with an agent card, then "NEW HIRES" cards |
| 10.5-16.4 | So what is it? Well, it's called agency agents. | real GitHub page crop, then big "AGENCY AGENTS" title |
| 16.4-22.2 | ...blowing up on the internet with over 160,000 stars on GitHub. | Star button 166k, big counter 160,224 |
| 22.2-29.4 | It's not one assistant. You get 280 AI specialists, like a whole company inside Claude. | grid of 283 tiny cards, then bar chart of divisions |
| 29.4-46.6 | outbound agent writes cold emails / sales team preps calls and proposal / engineers build the product / social, design, support | one card per role: agent card + drawn output (email, checklist, app UI, phone post, support ticket) |
| 46.6-61.5 | But then there's the craziest one, the orchestrator. It runs the whole project, hands the work to the right specialist, checks every step before it moves on. So you stop asking one AI to be everything. | hub with spokes (3D), then 4-step list PM > UX architect > Dev-QA > integration with ticks, a quote from the orchestrator file |
| 61.5-69.6 | The setup is simple. One install drops all of them into your laptop. Comment "agency" and I'll send you the link. | laptop with install counter, title card, comment-bait pill |

## Our script (same shape, honest words; present tense; voice-safe: no TH/R-cluster words where a plain one exists)
1. Claude Code just got 280 free AI specialists.   (HOOK, subject + stake at once; "free" and a number)
2. It's like a whole company living inside Claude.
3. It's called Agency Agents, and it has over 160,000 stars on GitHub.
4. It's not one assistant. It's 280 specialists.
5. One writes your cold emails.
6. A sales team preps your calls and writes proposals.
7. Engineers build the product.
8. Others grow your social media, design, and handle support.
9. But the craziest one is the orchestrator.
10. It hands the work to the right specialist and checks every step before it moves on.
11. So you stop asking one AI to do everything.
12. The install is one command, and you can add just one.
13. The setup's in the link in bio.   (locked line)
14. Want the next one? Follow.   (plain follow invitation, no promise)
Rough length 38-42 s, shorter than the reference (69 s) and shorter than 103 (46.7 s).
What we do NOT say: "run your whole business", "employees who work 24/7", "without hiring anyone", "make more money", "I'll send you the link". What is true and sayable (checked 15.11 and 17.11): free, MIT, 169.0k stars, README says "230+" agents while its tables link 283 (say "280" as the reel does? we say "about 280" in the caption, the voice says "280 specialists" only if the on-screen counter reads 283: decide), the orchestrator file exists and describes a software pipeline, one agent can be installed alone.

## Caption draft (under 2,200 chars; limits stated)
Claude Code just got 280 free AI specialists.

Agency Agents is a free, open-source library of about 280 ready-made role prompts for Claude Code: sales, marketing, design, engineering, support. Each one is a text file that tells Claude how to work as that specialist. It has over 160,000 stars on GitHub (169.0k when we looked on 17 November 2026).

The craziest one is the orchestrator: a prompt that tells Claude to hand a software project step by step to the other specialists (planner, designer, developer, tester) and check each step before moving on.

Setup: the exact steps, the repo link and how to install just ONE agent safely are in the link in bio.

Limits, said plainly: these are role prompts, not employees. They write drafts and plans; they cannot send an email or post anything unless you connect other tools. The "installs all of them" default adds ~280 files from a third party to every project, so read a file before you use it and start with one. We did not run them for this video; everything comes from the project's own page.

Save this for the day you need a second pair of eyes, and send it to someone who builds with Claude Code.

#claudecode #claudeagents #opensource #aitools #aiagents

## /e/104 setup path (English only on the site; from `channel/ref-agency-agents-verify-2026-11-15.md`)
1. Open github.com/msitarzewski/agency-agents and pick one agent from the README table (for example testing / Reality Checker).
2. Click the file, click Raw, read the whole text for anything that asks to run commands, open links, send data or change settings.
3. In Claude Code, ask: "Create .claude/agents/reality-checker.md with this text" and paste it.
4. Under `description:` add one line `tools: Read, Grep, Glob` so the agent can read but not run commands, edit files or use connectors.
5. Use it by name: "Use the reality-checker agent to review X."
6. Optional: install several with `./scripts/install.sh --tool claude-code --agent <id> --dry-run` first and read the plan. Never run the script with no flags.

## Visual direction (Miki style, real logos, no Claude-cuts-app gag, no black wipes)
- Frame 0: real Claude Code + GitHub marks and the number 280, text mostly visual.
- Counter 0 > 283 while tiny role cards fill a wall (real count, read from the README table), then a bar chart of divisions (real numbers: engineering 66, specialized 59, marketing 37 ...).
- One card per role with a drawn, labelled-example output; screens are labelled "example".
- Orchestrator: hub with spokes (3D feel, as in 103 but a different object: one pawn in the middle, specialists around it) and the 4-step list with ticks, quote taken from the real orchestrator file.
- Real GitHub page crop with the star count read the same day.
