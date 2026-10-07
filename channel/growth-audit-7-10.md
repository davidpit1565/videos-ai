# Growth audit against outside skills (7.10.2026)

David asked for one thing: go through the skills.sh directory (the link a commenter posted,
`vercel-labs/agent-skills` plus skills.sh), find the skills that cover short-form growth, and
check our system against them. Nothing was installed. The skill files were read as plain text
only. The goal is followers, not views. Roni (Videya) said the videos are fine but there is
"no strategy".

## What was actually checked

- `vercel-labs/agent-skills` itself is 8 coding skills (React, Vercel cost, web design,
  writing). **None of them touches content or growth.** The "hundreds of thousands" number is
  the skills.sh directory as a whole, not this repo.
- I searched skills.sh for instagram, reels, short-form, tiktok, viral, hook,
  content-strategy and social-media, and read these in full:
  - `vyralcontent/content-skills/viral-instagram-reels` + its references (`diagnose-flop`,
    `sends-playbook`, `reels-hook`, `insights`). This is the closest fit, but it has only
    ~11 installs and it advertises a paid tool (Vyral). I used the frameworks and ignored
    the pitch.
  - `coreyhaines31/marketingskills/social` (~73k installs) and `.../video`.
  - `social-media-skills/skills/short-form-video-script` (the WATCH framework).
- **Labels used below:** FACT = from our own data or files. SKILL = what the outside skills
  say (they are pattern guides, and their numbers come from vendor blogs). HYPOTHESIS = my read.

## The diagnosis, in the order the Reels skill says to run it

`diagnose-flop.md` says to stop at the earliest lever that explains the result. Our numbers
(FACT, `content-memory.md`):
- Episode 55: 260-447 views, about 51% from the Reels tab (cold audience), and **0 followers gained**.
- About 60% of viewers are gone by 2s, ~12% are left at 10s and ~3-4% at the end.
- Followers have been flat at 122-123 for a week, whatever the views did.

1. **Originality:** probably fine. Our footage is heavily edited and has no third-party
   watermarks. UNKNOWN: whether Unsplash stock photos plus a synthetic voice count against
   us under Meta's originality rules. No check can settle this from here.
2. **Hook, the 3-second cliff:** **this fails.** SKILL: the first frame needs a 3-5 word
   headline that is fully on screen at frame 0, with visual, spoken and text hooks all
   landing inside the first second. FACT: episode 59's hook is 12 words, and the template
   builds it word by word. The episode-60 experiment already targets this, so keep it.
3. **Body:** we cannot read this yet, because the hook cliff hides everything after it.
4. **Topic legibility ("views without follows"):** **this fails, and it is the lever that
   matches our exact symptom.** SKILL: when a Reel gets real reach and close to zero
   follows, the stranger could not tell what the account is for. The bio, the grid and the
   topic have to promise "more of this". FACT: the last 15 episodes jump between Alexa,
   ChatGPT memory, resume software, a scam video, LinkedIn, WhatsApp and Meta. The 59
   episodes before them include n8n tutorials and `voice_doctor.py`. There is no named
   series, no single promise, and the closing line ("Follow, so you get the full story")
   gives no reason that only this account can offer. **This is most likely what Roni
   meant by "no strategy".**
5. **Send signal:** partly fixed already. We use named-person send-prompts ("Send this to a
   friend who's looking for a job"), which is the exact pattern the skill recommends.
   What is still missing is a *memorable container*: a recurring name a viewer can repeat
   in a DM ("the switch"). SKILL: a useful tip with no name does not get forwarded, and a
   named one does.
6. **Audio:** not relevant. The music is licensed, and the account can confirm it plays.
7. **Caption:** small issue. SKILL: the first line of the caption should be the plain
   keyword phrase ("LinkedIn AI training setting"), not the hook. We use 5 hashtags, which
   is the working ceiling.

## Where our own rules disagree with all three skills

- **Length.** CLAUDE.md says 45-75s and never under 30s. That rule rests on Buffer's and
  Socialinsider's studies. All three skills put Reels at **15-35s**. Our own retention
  curve has ~12% of viewers left at 10s, so a 60s episode is mostly unwatched. This is a
  real conflict, and one study should not overrule the other. **Test it** with a 20-30s cut
  of the same episode (see below). Do not just flip the rule.
- **The ending.** We stack three closing beats: send-prompt, "The setup's in the link in
  bio", and the tomorrow/follow line. Together they take about 10 seconds, at the point
  where 3-4% of viewers are still watching. SKILL: use one CTA of about 2 seconds, and
  don't close on the creator. HYPOTHESIS: move the send-prompt to right after the payoff
  (~15s) and keep a single closing line.

## What no pipeline in this repo can do, and every skill lists anyway

- **A person.** All 59 episodes use a cloned voice over stock photos, with no face on
  screen, ever. SKILL: a face with a clear expression is the strongest first frame, and
  the content plans set ~15-25% personal and behind-the-scenes posts. HYPOTHESIS, a strong
  one: people follow a person they can picture. An 18-year-old in Belgium building an AI
  business is itself a story, and none of our competitors can copy it.
- **Daily engagement and collabs.** SKILL (`social`): 30 minutes a day. Reply to every
  comment in the first hour, leave real comments on 5-10 posts from accounts in the
  niche, build ties with 20-50 accounts, then collaborate. FACT: comments total 8 across
  45 episodes. The word "collab" appears once in `content-memory.md` and has never been
  tried. An Instagram Collab post appears on both accounts' feeds. It is the only lever on
  this list that does not depend on the algorithm.

## Recommendations, ranked by expected effect on followers

1. **Decide the positioning, in one sentence. This is David's decision, not a guess.** It
   should name who the account is for, what they get, and why they should follow. Then put
   that sentence in the bio, pin 3 posts that prove it, and run a named series every
   episode lives inside. Example only: *"The AI switches companies turned on for you, and
   how to turn them off."* That matches what 55/57/58/59 already are.
2. **The first 3 seconds** (episode 60, already planned): a 3-5 word headline on screen at
   frame 0, the voice starting at 0.0s, and the payoff inside 2 seconds.
3. **Test a short cut:** the same episode at 20-30s against our usual ~60s. Measure at
   equal age: % still watching at 3s, average watch time, sends, and followers from the post.
4. **One closing beat**, with the send-prompt moved earlier. This changes two locked
   closing-line rules, so it needs David's approval.
5. **His face in the first 2 seconds of one episode** as a test, with the rest built as usual.
6. **30 minutes a day of real engagement, plus 1-2 Collab posts.** Only David can do these.
7. **Measure what the diagnosis needs.** Per Reel in Insights: *followers from this post*,
   *skip rate* and *profile visits*. Our tracker (`studio/lib/sources.ts`) pulls views,
   reach, saves, shares and watch time, but not these three. UNCONFIRMED: whether the
   Graph API exposes them for Reels. Until that is checked, David reads them from the app.

## Not recommended

- Installing the skills. Their useful content is captured above, and the Vyral ones carry
  an upsell.
- Paid boosting (`content-memory.md`, 23.9.2026: validate a format organically first).
- A virality score.
