# Skill vetting (9.11.2026), manual (NVIDIA SkillSpector install was blocked by the environment's permission classifier)
Method: shallow clones in scratchpad, grep for curl|sh, eval/exec, base64 -d, ignore-previous-instructions, rm -rf, sudo, ssh keys, env/API-key reads, webhooks, then read SKILL.md heads. Limits: grep is not a full scan; no LLM pass.
- iart-ai/motion-design-skills@motion-art-direction (4.8K installs): 3 markdown files, no scripts, no hits. OK.
- iart-ai/kinetic-typography-skills@kinetic-typography (3.4K): 3 markdown files, no scripts, no hits. OK.
- barty-bart/motion-graphics@sound-effects (2.6K): 117 files, 110 CC0 sound effects (LICENSES.md lists Kenney + Freesound CC0 sources), 2 python scripts. One finding: scripts/sound_pass.py uses eval() on ffprobe's frame-rate string (low risk, local data, fix = fractions.Fraction); one sound is fetched at runtime from mixkit. No exfiltration patterns. OK with that fix.
- heygen-com/hyperframes@hyperframes (1.4M): the HyperFrames skill we already build on. Only env reads for Chrome path and render params. OK.
- coreyhaines31/marketingskills social: no hits; we already have 'social'.
- vincentwei1021/video-shotcraft (8K): 1,220 files, Remotion-based, Chinese docs, 23 scripts. NOT vetted in depth: skipped.
Installation into ~/.claude/skills was blocked by the permission classifier ([Untrusted Code Integration]); not worked around. Cloned copies stay in scratchpad skillscan/ and can be read as reference.
