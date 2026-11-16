# Reel DfQDKhNzXtm: "Claude just destroyed paid apps" / the Replica skill (seen 16.11.2026)

David wants a video on it AND to use the tool himself. Nothing installed. Contact sheet: `channel/assets/refs-2026-11-16/DfQDKhNzXtm-sheetA.jpg`; transcript and frames in the session scratchpad `refs16/DfQDKhNzXtm/`.

## The reel (facts)
- Account **@auraguy.ai**, 2.11.2026, 67.7 s, 3,247 likes, 2,722 comments (keyword "CLONE").
- Script (faster-whisper): "Claude just destroyed paid apps. You can now clone any app with Claude, so you never have to pay for a subscription again. And it's completely free ... It's called the replica skill, and it's not one skill, it's 11 ... like a little dev team living inside Claude. The first one reverse-engineers the app you want to clone. Another one rebuilds it, screen by screen. One handles the backend, and one tests it for bugs ... But then there's the craziest one, the entrepreneur skill ... reads real user reviews to find the missing features, the unsolved problems, and everything people hate. Then it fixes all of that in your app, so you end up with an app you can actually sell. And the setup? Almost too easy. Paste the repo link inside Claude and say, install skill ... it rebrands your version before launch, so it's your own brand, not a copy. If you want the skill, just comment clone."
- Opener: the Claude starburst knocks three real app tiles (Slack, a blue "C" app, Notion) which shatter, with a small "Logos: their respective owners" note top-right. Same template as `ref-2026-11-16-DfK1boQTr6t.md`.
- The GitHub page shown on screen: `github.com/Jakeschincariol/replica-skill` (live page, dated "Nov 2, 2026").

## The repo, verified (read through Exa from the GitHub page, 16.11.2026; the GitHub API was not open to this session)
- Real: **Jakeschincariol/replica-skill**, MIT, **9,512 stars, 1,709 forks**, 37 open issues, created 3.10.2026, Python + TypeScript, homepage opusjake.ai. Same author as our installed `ig-*` skills.
- Caution on the numbers: the contributor list shows the author with **1 contribution** (a single-commit repo) next to 9.5k stars in six weeks. Viral reels from @auraguy.ai alone could explain fast stars; organic or bought, we cannot tell. Read the star count the same day before any number goes on screen, and do not present stars as proof of quality.
- What it is: 11 skill folders (SKILL.md instructions) that run in order and write into a `replica/` folder: recon (screens, flows, data model from public pages and your own account) -> architect (stack, schema) -> design (tokens) -> build -> backend (auth, payments) -> test (Playwright specs) -> diff (parity score) -> entrepreneur (themes from real reviews you supply, every quote linked) -> brand (new name, palette; trademark checks to run) -> launch (landing page, store listing) -> deploy.
- Six helper scripts, standard-library Python, the README says none touch the network: `imgdiff.py`, `parity.py`, `reviews.py`, `contrast.py`, `sweep.py` (finds the original's name/colours left in your code), `listing.py`. Tests included.
- Install (README): paste the repo URL into Claude and say "install skill"; or in Claude Code `/plugin marketplace add Jakeschincariol/replica-skill` then `/plugin install replica-skill@replica-skill`; or `git clone` and copy `replica-*` folders to `~/.claude/skills/`. Anthropic's own docs (code.claude.com/docs/en/plugins/install, read 16.11.2026) confirm the `/plugin marketplace add owner/repo` + `/plugin install name@marketplace` mechanism; in a session `/plugin install` opens a review panel before installing.
- Fine print (README): rebuilds features and flows "clean-room style", never code, logos, copy or content; reads only public pages and your own account; refuses scraping behind logins; forces a rebrand before deploy; "talk to a lawyer before launch ... not legal advice".

## Where the reel overclaims (do not repeat)
- "Clone any app ... never pay for a subscription again": the README itself says a booking tool is "weeks" of work and a spreadsheet engine is not realistic; you still pay for hosting, a database, Stripe, a domain, and a Claude plan with Claude Code; and you maintain it. Untested by us.
- "An app you can actually sell": legal and trademark risk is real (the README says so). "Completely free" = the skill is free; the work and the Claude usage are not.

## Risks if David uses it himself
1. It is third-party instructions that Claude will follow on his machine: read each SKILL.md before installing; install the plugin in a test folder (local scope), not globally.
2. The deploy and backend skills touch payments, keys and DNS: secrets go only where our rules say (never in chat/git).
3. Token cost: 11 stages on a real app is a lot of Claude usage (his credits).
4. Cloning a named competitor and selling it: trademark/terms risk; use it on an app idea, not on a brand.

## How it could serve OUR pipeline
- `/replica-entrepreneur` on David's own app Flow (App Store id 6807543350) or on a competitor: a ranked list of what users hate, every quote linked. Useful for the business side, not the reels.
- `/replica-recon` + `/replica-diff` on our studio vs a paid scheduling/analytics tool: an honest parity test is a ready-made episode ("Can Claude rebuild a $X/month app in one evening? Parity score 62/100").
- `imgdiff.py` (layout diff ignoring colour) could compare a rendered frame with a reference frame: an idea for Miki-style checks, not needed now.

## Video angle (rough, see `channel/queued-ideas.md` Q4)
- TOPIC verdict: money people already pay (subscriptions) + "Claude can rebuild the app" is felt in 3 s by anyone with a subscription; proof is possible (our own test). Better than a plain feature list.
- Honest version = our own test: pick one small paid app type (a link-in-bio page or a booking page), run recon -> build -> diff, show the real parity score and the real time/cost, then "the craziest one": the entrepreneur skill's real top-3 complaints with linked reviews.
- Hook options (statements, surprise first): "This subscription? Claude rebuilt it tonight." / "Claude cloned a paid app. Here's the score."
- Opener: the Claude mark cuts the paid app's real logo in two (the cut gag from DfK1boQTr6t) only if the result supports it; otherwise show the parity score as the reveal.
- Duplicate check (16.11.2026): `topics-covered.txt` has 41 "ChatGPT can now see every subscription draining your bank account" and 50 "You have no idea how much you're actually paying in subscriptions": same money theme, different angle (those are about seeing subscriptions, this is rebuilding the app); no hit for clone/replica/rebuild. `content-memory.md`: no hit.
- Funnel: TOP/MID. Risks: a long test before any building; legal wording ("an alternative you own", never "a copy of <brand>"); the real result may be weak (then the video says so, or we drop it).
