# Avatar wardrobe — same face, scene per episode topic

Every file here is the same generated person (kept consistent across separate
ChatGPT image-edit passes, referencing the approved base photo each time so
the face doesn't drift) — the D-ID avatar host for episodes that use the
talking-head format instead of the usual animated-typography build.

`avatar-01-amber-default-fullres.png` is the approved default, submitted for
episode 26. The rest are a wardrobe to match a future episode's specific
topic — pick by the "use for" column, not just whichever looks best.

| File | Use for |
|---|---|
| `avatar-01-amber-default(-fullres)` | default — most episodes |
| `avatar-02-tech-casual` | everyday/casual episodes |
| `avatar-03-collared-neutral` | slightly more formal than 02, still everyday |
| `avatar-04-cool-blue` | bug/failure episodes |
| `avatar-05-warm-bright` | success/solution episodes |
| `avatar-06-wet-watermarks` | watermark-related topics (literal visual pun) |
| `avatar-07-particles-agents` | AI agents / agentic workflows |
| `avatar-08-glass-transparency` | audit / transparency / verification topics |
| `avatar-09-double-shadow-retry` | retry/duplicate/idempotency topics (episode 25's own subject) |
| `avatar-10-chain-workflow` | automation / n8n / workflow-chaining topics |
| `avatar-11-disintegration-ai-reveal` | "this is AI" reveal moments |
| `avatar-12-gears-efficiency` | speed / efficiency topics |
| `avatar-13-bright-eyes-reflection` | code / technical-tool topics |
| `avatar-14-red-urgent` | urgent/warning episodes |
| `avatar-15-gold-triumphant` | confident wins |
| `avatar-16-suspense-dark` | slow-build reveal / suspense cold opens |
| `avatar-17-corporate-suit` | business/selling-to-clients topics |
| `avatar-18-tech-jacket` | modern technical topics, between casual and formal |
| `avatar-19-plain-tshirt` | most casual/accessible episodes |
| `avatar-20-1920s-suit` | "principles/fundamentals" episodes |
| `avatar-21-coins-cost` | pricing / cost-savings topics |
| `avatar-22-lock-security` | security / privacy topics |
| `avatar-23-motion-blur-speed` | speed / automation topics |
| `avatar-24-split-comparison` | A-vs-B / this-vs-that comparison topics |
| `avatar-25-circuit-api` | API / integration topics |
| `avatar-26-soundwave-audio` | voice / audio topics |
| `avatar-27-second-face-teamwork` | multi-agent / teamwork topics |
| `avatar-28-grid-data` | data / analytics topics |
| `avatar-29-city-bokeh-mobile` | mobile / on-the-go topics |
| `avatar-30-crack-warning` | mistake / warning episodes |
| `avatar-31-magnifier-search` | search / discovery topics |
| `avatar-32-sparkle-milestone` | milestone / anniversary episodes |

Public at `https://www.actually-works.com/avatars/<file>` (registered in
`studio/lib/routes.ts` — D-ID's `/talks` API fetches `source_url` itself,
outside any browser session, so these can't sit behind the studio's PIN).
