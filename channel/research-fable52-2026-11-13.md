# Research: Claude Fable 5.2 and what people did with it

Researched 12-13 Nov 2026 (live web search, pages opened). Not a script. Nothing here was tested by us.
Status labels: CONFIRMED (primary source read) / REPORTED (news or blog, not a primary source) / ONLY SOCIAL (a creator's own post) / NOT FOUND / UNVERIFIED.
"Confirmed" means "the source really says this", not "the claim is true". Every Anthropic claim below is the vendor's own claim.

Repo check: `grep -i "fable\|5.2\|new model" channel/topics-covered.txt` returned no matches. No earlier episode covers this model.

## 1. Official facts (Anthropic)

| Claim | Status | Source URL | Exact quote |
| --- | --- | --- | --- |
| Announced 9 Nov 2026 | CONFIRMED | https://www.anthropic.com/news/claude-fable-and-mythos-5-2 | "November 9, 2026" / "We've upgraded Claude Fable and Claude Mythos—models that are designed to tackle the most daunting technical challenges." |
| Fable and Mythos are one model; Fable is the public one | CONFIRMED | same | "Claude Fable and Claude Mythos are the same underlying model. Fable has strong cybersecurity and biology safeguards to guard against misuse, which allows us to make it available to all users." |
| What improved | CONFIRMED | same | "Claude Fable 5.2 and Claude Mythos 5.2 show improvements in areas like coding, reasoning, and vision." |
| Speed and API price | CONFIRMED | same | "They generate outputs up to 30% faster than Claude Fable 5.1 and Claude Mythos 5.1, and they're available at a lower price: $8 per million input tokens and $40 per million output tokens." |
| Where available | CONFIRMED | same | "available today on all platforms, including Amazon Web Services, Google Cloud, and Microsoft Azure" (model ID `claude-fable-5-2`) |
| Plans: paid only, not Free | CONFIRMED | https://support.claude.com/en/articles/15424964 | "Claude Fable 5.2, Claude Fable 5.1, and Claude Fable 5 are available on all paid plans (Pro, Max, Ultra, Team, and Enterprise)." / "Fable models aren't available on the Free plan." |
| Plans: included on Max/Ultra, pay-as-you-go on Pro | CONFIRMED | same | "Pro plans and standard seats on Team plans: Fable models aren't included in your plan's usage limits. You can use them with usage credits" |
| Launch-week offer for Pro | CONFIRMED (launch post); end date 16 Nov only REPORTED (smartscope.blog; Anthropic's offer page timed out) | https://www.anthropic.com/news/claude-fable-and-mythos-5-2 | "Fable is included for up to 50% of weekly usage limits for Pro plans and standard seats on the Team plan." |
| Anthropic itself says: not the everyday model | CONFIRMED | same | "For most coding and knowledge tasks, we recommend that users start with Claude Opus 5.5, our strongest daily driver" |
| Headline benchmark | CONFIRMED (Anthropic's own table) | same | "At Xhigh effort, Fable 5.2 reaches 49.1%, the highest score of any released model we've tested." (FrontierCode 2.0; Opus 5.5 45.5%, GPT-6 Astra 42.8%) |
| Not best on everything | CONFIRMED | same (table) | AutomationBench: Fable 5.2 51.4% vs Gemini 4 Carbon 53.9%; AA-Briefcase Elo: Fable 5.2 1785 vs Opus 5.5 1800 |
| Operating system demo | CONFIRMED (internal experiment, no outside test) | same | "the model coordinated over 1,000 subagents, working around the clock for eight days... It produced a working operating system that boots on a laptop" |
| Fermat's Last Theorem formalized (maths, in Lean) | CONFIRMED | same | "a team of 1,000 Fable 5.2 agents fully formalized the theorem in just 30 hours, with minimal human intervention." |
| Three electronic devices | CONFIRMED | same | "All three devices worked without needing any electrical modifications." (built with Diode) |

## 2. The physics claim ("solved physics problems open for years")

Verdict: the rumour has a real source. Anthropic itself claims it. It is NOT independently verified.

| Claim | Status | Source URL | Exact quote |
| --- | --- | --- | --- |
| Anthropic says it solved two open physics problems | CONFIRMED (vendor claim) | https://www.anthropic.com/news/claude-fable-and-mythos-5-2 | "Claude Fable 5.2 solved two open problems in theoretical physics. Both concern black holes" |
| Problem 1: a calculation laid out in 2003, never finished | CONFIRMED (vendor claim) | same | "A calculation to determine whether the same was true in very small universes... was laid out in 2003 but was too laborious to complete. Fable 5.2, working largely autonomously, completed it and found the transition is abrupt there, too." |
| Problem 1 preprint: 42 pages, result b = -1.48e-3 lambda^2 | CONFIRMED | https://hexagonmath.org/2611.00175v1 | "It first appears at three loops and, to our knowledge, has not been computed in the two decades since. We find b=−1.48×10⁻³ λ²... The transition is first order." |
| Problem 1: who did it and who checked | CONFIRMED | same (provenance statement) | "An internal Claude research model, prompted by a physicist, obtained the result presented here. The physicist checked it against several known special cases. A separate Claude computation using a different method, not included here, gives the same result." |
| Problem 2: exact limit of a technique used 15+ years | CONFIRMED (vendor claim) | Anthropic post | "Fable 5.2 found the exact limit of a technique physicists have used for more than 15 years to rule out candidate theories of quantum gravity in a simplified universe." |
| Problem 2 preprint: 131 pages, number was between 8.503 and 12, now about 9.1266 | CONFIRMED (abstract read, paraphrased by fetch tool; number repeated by 4 outlets) | https://hexagonmath.org/2611.00174v1 | Provenance: "The main result was first obtained autonomously by an internal Claude research model. The publicly available Claude Opus 5.5 later obtained the same result independently. Claude then wrote this paper, following brief guidance from a physicist, who also checked every main result." |
| Which model did it is not fully clear | CONFIRMED mismatch | both preprints vs launch post | Launch post says "Fable 5.2"; preprints say "an internal Claude research model"; paper 2 was also reproduced by Opus 5.5 |
| Peer reviewed | NOT FOUND (no review; v1 preprints on Hexagon, a new server; not on arXiv) | https://aiprovedwhat.com/episodes/an05-modular-bootstrap-large-c/ | "The paper is not on arXiv, not peer reviewed, has no Lean proof, and its interval-arithmetic code is not published. We found no expert reaction yet." |
| Named outside physicist confirming or disputing | NOT FOUND (searched 12-13 Nov; the checking physicist is unnamed) | https://www.justaparrot.com/e/claude-black-hole-physics/ | "Neither preprint is peer reviewed, and we found no named outside physicist confirming or disputing them." |
| Sceptic points | REPORTED | https://aitoolsrecap.com/Blog/claude-fable-5-2-black-hole-physics-problems-solved ; https://stateofproof.org/paper-watch/hexagon-2611-00175 | "that second computation also came from a Claude model" / "The paper reports an unresolved mismatch in one pure Yang–Mills comparison" / justaparrot: "Anthropic does not say how many other problems were tried without success." |
| Scope: theory only, not real black holes in space | REPORTED | https://magica.com/news/anthropic-claude-fable-black-hole-physics-claims | "It does not establish how all astronomical black holes form." |
| "23 years" figure | REPORTED only (nerdzap, cryptobriefing: 2003 to 2026). Anthropic says "laid out in 2003"; the preprint says "two decades" | https://nerdzap.com/news/claude-fable-mythos-5-2-black-hole-physics/ | "a laborious calculation that had gone unsolved for 23 years" (outlet wording, not found in Anthropic's text I read) |
| Mainstream science press (Nature, Quanta, New Scientist) coverage | NOT FOUND in my searches | - | - |
| Earlier Claude physics result with a NAMED checker (context, different model, Sept 2026) | REPORTED (physicist blog) | https://www.math.columbia.edu/~woit/wordpress/?p=15881 | "This was sent on September 1 to Lance Dixon, who had techniques that allowed him to validate the result." / "It appears that Claude did not come up with a new method, just used known calculational methods." |

## 3. Things people did with it that spread

All view counts below are as REPORTED by TalkEsport (10 Nov); I did not see the X counters myself: "not seen".

| Claim | Status | Source URL | Exact quote |
| --- | --- | --- | --- |
| Launch post on X: 12.6M views | REPORTED, count not seen | https://www.talkesport.com/editorials/claude-fable-5-2-games-ai-game-development/ (post: https://x.com/claudeai/status/2119899484373369278) | "its announcement post passed 12.6 million views by Tuesday" |
| First-person shooter by Felix Rieseberg (Anthropic employee), close to 1M views | ONLY SOCIAL + REPORTED, count not seen | same (X @felixrieseberg, 9 Nov) | "Everything in this game is from scratch: models, sounds, textures. ~$550 at API pricing, ~2.7M output and 445M input tokens, heavily cached. Took 8 hours!" |
| Browser boat ride through eight worlds by Kevin Ngo, 320,000 views | REPORTED, count not seen | same | "a boat ride through eight dreamlike worlds, playable in the browser, which passed 320,000 views" |
| GTA-style city "one prompt, 2 h 14 min, $200 plan" (@ericmaskfr) | ONLY SOCIAL, count not seen; his "$90,000 and 8 months" comparison is unsourced | same | "a figure he did not source" |
| Nephew's beat 'em up game built overnight from a child's drawings | REPORTED; 448 Hacker News comments seen on aggregator | https://zeli.app/story/50433659 | "Around 340M tokens later, the family was playing four-player co-op." |
| Matt Shumer thread: voxel engine, "Mirror Earth", "Hogwarts Royale" | ONLY SOCIAL, counts not seen, no independent test | https://explainx.ai/blog/top-20-things-built-with-claude-fable-5-2-matt-shumer-anthropic-mollick-2026 | "I spent over 400B tokens testing Fable 5.2" / "we found no independent testing" |
| Excel clone, video editor, Fall Guys-style game with large costs | REPORTED (single blog, cost figures are that blog's estimates) | https://www.mindstudio.ai/blog/fable-5-2-vibe-coding-demos/ | "The Gears of War clone used an estimated 12+ billion tokens and ran close to $15,000 in equivalent API cost." |

## 4. What makes claims risky

| Risk | Status | Source URL | Exact quote |
| --- | --- | --- | --- |
| Anthropic edited the launch post on 11 Nov (Fermat section) | CONFIRMED | Anthropic post | Edit note: "Amended a sentence and added a footnote to the 'Mathematical formalization' subsection"; footnote 4: agents got "a list of 60 statements, a one-sentence sketch of the classical route" plus 47 proved lemmas |
| "One prompt" is misleading: hours, many agents, hundreds of dollars | REPORTED | explainx.ai link above | "The headline says one prompt, the footnote says many agents." |
| Viral demos come from insiders and sellers | REPORTED | talkesport link above | "Many of the most viral clips also came from people with early access, enthusiast accounts or companies that sell AI tools." |
| Benchmarks are self-reported; outside evaluators did not endorse the post | CONFIRMED | Anthropic post, footnote 5 | "None of the external organizations reviewed the contents of this blog post or the contents of the System Card." |
| Robotics score run internally | CONFIRMED | Anthropic post | "RoboDojo Sim shows the highest-available effort and was run internally." |
| Single run for the Fermat comparison | CONFIRMED | Anthropic post | "a single run per model" |
| Franchise clones (GTA, Harry Potter, Gears of War) carry copyright risk if shown | REPORTED | talkesport link | "Activision did when it shut down AI-built Call of Duty browser ports in October" |
| Retraction of the physics papers | NOT FOUND (none as of 13 Nov) | - | - |
| Several low-quality blogs mislabel things (e.g. MindStudio calls it "Claude Opus 5.2" and calls Opus 5.5 its predecessor) | CONFIRMED sloppy secondary source | https://www.mindstudio.ai/blog/claude-opus-5-2-science-discoveries | do not quote these blogs as fact |

## Safe to say in a video

- "Anthropic says its new model, Claude Fable 5.2, solved two open physics problems about black holes." (always with "Anthropic says")
- "One was a calculation set out in 2003 that nobody finished." (Anthropic's wording: "laid out in 2003 but was too laborious to complete")
- "The other: a number physicists only knew was between 8.5 and 12. The paper says it is about 9.13."
- "No outside physicist has confirmed it yet. The papers are not peer reviewed." (true as of 13 Nov 2026; re-check on publish day)
- "The papers were written mostly by AI and checked by one unnamed physicist."
- Released 9 Nov 2026; paid plans only; $8 / $40 per million tokens on the API.
- "An Anthropic employee says it built a playable shooter in 8 hours for about $550." (his own claim, attributed)
- "Anthropic itself tells most people to start with a different model, Opus 5.5."

## Do NOT say

- "AI solved physics" / "proved" / "confirmed" / "scientists verified". Nobody outside Anthropic has.
- "Solved a mystery about real black holes." It is a result in an idealized theory, not space.
- "Open for 23 years" as Anthropic's number. Say "set out in 2003".
- "Fable 5.2 did it alone." The preprints say "an internal Claude research model", prompted and checked by a physicist; Opus 5.5 also reproduced one result.
- "Built a game from one prompt in seconds" or "free". It took hours, many agents, hundreds to thousands of dollars.
- Any view count as our own measurement; any "$90,000 and 8 months" comparison.
- "Best at everything" or "beats GPT-6 on every test". Anthropic's own table shows it losing two rows.
- Do not show GTA / Harry Potter / Gears of War clone footage (other people's work and third-party IP).
