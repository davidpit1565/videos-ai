# Claude Motion: facts (checked 12.11.2026, live scrape, maxAge 0)
Sources: A = https://claude.com/resources/articles/dashboards-and-motion (published 2026-10-08, "Starting today")
         B = https://support.claude.com/en/articles/17454997-get-started-with-claude-motion

## Quotes
(a) What Motion makes and from what input
- A: "Ask Claude to turn a quarterly report into a 30-second explainer for an all-hands, add motion to a chart in a board deck, or make a product walkthrough for customer onboarding. Claude builds an animation from your prompt, and it plays like a short video."
- B: "Claude Motion turns your content into short animations, like an explainer for an all-hands, an animated chart for a board deck, or a product walkthrough for customer onboarding."
- B: "Attach the report, data, or images you want Claude to use, so the animation is built from your own content."
- B: "Say who will watch it, where it will play, and roughly how long it should be."
- PDF is NOT named anywhere on either page. Named inputs: prompt, quarterly report, content, report, data, images, setup steps.
(b) No video model
- A: "It doesn't use a video generation model, so there's no generated footage and no AI-generated people."
- A: "Claude writes code that animates your text, charts, shapes, and images, so you can change any word, number, or timing."
- B: "Claude Motion doesn't use a video generation model, so it doesn't create realistic footage or people."
(c) Editing one word/number/timing
- A: "...so you can change any word, number, or timing."
- B: "Because each animation is code, you can change one detail, like a word, a number, or the timing, and the rest stays as it was."
- B: "Ask for changes in the chat, like "Slow down the second scene" or "Change the Q3 number to 18%.""
(d) MP4
- A: "You can adjust it in the editor or ask Claude to change it, then download it as an MP4 file."
- B: "To download an animation, click "Export" and choose MP4."
(e) Plans and launch
- A: "Claude Motion is in beta on Team and Enterprise."
- B: "Claude Motion is available in beta on Team and Enterprise plans. It's on by default on Team plans. On Enterprise plans, it's off by default until an owner turns it on in Organization settings > Artifacts."
- Launch: A is dated 2026-10-08 (page metadata publishedTime) and opens "Starting today, Claude can turn your data into a dashboard that stays current, and your ideas into an animated explainer for your next presentation." So Motion launched 8 Oct 2026 (date from page metadata, the text only says "today").

## Verdicts on the draft lines
1. "Claude turns a boring PDF into a video."  -> NOT OK as written. Anthropic never says PDF. It says report / content / data / images. Also Anthropic calls the output an animation that "plays like a short video" and exports as MP4.
   Corrected: "Claude turns a boring report into a short video." (or "...into an animated video").
2. "You give it your file, and tell it who is watching and how long." -> OK in substance. Anthropic: "Attach the report, data, or images" and "Say who will watch it, where it will play, and roughly how long it should be." Safer: "You give it your report, and tell it who is watching and how long."
3. "And there's no AI footage. Anthropic says it's all built with code." -> OK. Matches "no generated footage and no AI-generated people" and "Claude writes code that animates your text, charts, shapes, and images." Optional precision: "Anthropic says Claude writes code, not footage." ("all" is a slight stretch but consistent with "each animation is code".)
4. "It's in beta, for Team and Enterprise plans only." -> OK. Matches "in beta on Team and Enterprise". Caveat if space allows: on Enterprise an owner must switch it on (off by default). Do not say "Free/Pro can't" beyond "Team and Enterprise" as Anthropic words it; "only" is our inference from the two plans being the only ones listed (the help article lists no others).

## Not confirmed
- Whether PDF upload works in practice (not tested, not stated).
- Exact launch time of day; only the date 8.10.2026.
