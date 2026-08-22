# Episode 05 — "Claude Code from zero, on Windows"

**Format:** long-form YouTube (target 20–26 min) + a 50s reel
**Topic:** `claude code tutorial beginners` — **median 159,426 views**, second-highest measured
**Blocked on:** nothing.

**Why Windows.** Every course in this topic is filmed on a Mac, and the top result is a
four-hour Mac course with 2.3M views. The install is the part that differs and the part people
quit on. Filming it on Windows is not a gimmick — it is the gap in a topic with 159k median
demand.

---

## What it builds

Something small and real, on a project the viewer can see the whole of: take a folder of
inconsistently-named files and rename them to one convention, with a dry run first.

Chosen because the task is verifiable at a glance, it touches the filesystem so permissions
come up naturally, and a dry run is the reversible-first rule from episode 02 applied to a
tool that can actually delete things.

## The spine

| Section | On screen | The point |
|---|---|---|
| Cold open | The rename running, dry run then real | Proof before promise |
| Install | The actual terminal, the actual output | Windows, not a Mac |
| First run | The login, the first prompt | Where it starts |
| **The permission prompt** | The dialog, paused, read aloud | This is where people quit |
| The dry run | Asking for a plan before an action | The habit, taught once |
| The real run | Files change on screen | It works |
| **When it goes wrong** | It renames two files incorrectly. Kept in | Live |
| The undo | Getting them back | Why a dry run exists |
| The limits | What it will not do, and what it should not be trusted with | The honest close |

## The moment the episode exists for

**The permission prompt.** A tool that asks "can I run this?" is the single most common place a
beginner stops, because nothing on screen says whether saying yes is safe. So the video stops
there, reads the prompt out loud, explains what it is actually asking, and says plainly when the
answer should be no.

Almost no tutorial does this, because it interrupts the flow. It is the reason the tutorial gets
finished.

## The defect that stays in

It renames two files wrong — one because the pattern was ambiguous, one because a filename had
a character the convention did not account for. **Both stay in the cut**, with the fix.

A tutorial where nothing goes wrong teaches the viewer that going wrong means they broke it.
That is the belief this channel exists to remove.

## Numbers this episode carries

- **How long the install took**, timer on screen, from download to first working prompt
- **Files renamed correctly out of the total** — counted
- **What one run cost** — the real figure, whatever it is

## The reel cut (50s)

Hook is the prompt, not the feature: *"This dialog is where everyone quits Claude Code. Here's
what it's actually asking."*

## Not in this episode

- Agents, subagents, MCP, hooks. That is episode 09 onward, and putting them here is how a
  beginner tutorial becomes a features tour nobody finishes.
- A Mac section. The whole point is that this one is not filmed on a Mac.
- Any comparison against other coding tools. Different episode, different demand.
