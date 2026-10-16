#!/usr/bin/env python3
"""Cut a real, licensed music-library track to an episode's exact length —
same contract as build_music.py (a total duration in, a ready music.wav out),
so produce.sh can point at either one interchangeably.

Usage: python3 audio/pick_real_track.py <seconds> <out.wav> --mood <mood> [--no-record]
       python3 audio/pick_real_track.py --rotation-test <mood>   (10 simulated picks, writes nothing)

Moods map to files in audio/music-library/ (see MANIFEST.md for what each one
actually sounds like and its real source/license). A track shorter than the
requested length is looped (audio/music-library/trending-vibe--alexmorgan.mp3
is the one 22s case); a longer one is trimmed from its start. Either way the
same fade-in/fade-out as build_music.py's own output, so the two are
interchangeable in render.sh without retuning levels.
"""
import json, random, subprocess, sys, os, collections

LIB = os.path.join(os.path.dirname(__file__), "music-library")

# Rotation (16.10.2026): every pick is appended to last-used.json (git-ignored, last 5
# kept); a mood with more than one candidate never reuses a track from the last 3
# picks, and falls back to any candidate only if all of them were used recently.
HISTORY = os.path.join(LIB, "last-used.json")
HISTORY_KEEP = 5
NO_REPEAT = 3

# Each mood maps to a LIST of candidate files — pick_real_track.py chooses randomly
# among them (see main()) so two episodes landing on the same mood don't always get
# the identical track. Most moods still only have one real option; add more as
# David listens to and picks real tracks for them (see MANIFEST.md's TODO).
# Widened 16.10.2026 (channel/music-sourcing-prompt.md): 54 new Pixabay tracks, one list per
# first-guess mood. Mood labels are guesses from titles + loudness checks — not yet heard.
NEW = {
    "tense": [
        "tense--airium-tense--leberch.mp3",
        "tense--tense-suspense--leberch.mp3",
        "tense--suspense-tense-background-music--sigmamusicart.mp3",
        "tense--palladium-thriller--leberch.mp3",
        "tense--thriller-tension--leberch.mp3",
        "tense--suspense-tension-background-music--peacockmusic.mp3",
        "tense--chase-percussive--echobrainz.mp3",
    ],
    "punchy": [
        "punchy--punchy--themountain.mp3",
        "punchy--fresh-urban-stomp--osynthw.mp3",
        "punchy--punchy-brass-groovy-pop-track--moonpub.mp3",
        "punchy--trending-instagram-reels-music--bombinsound.mp3",
        "punchy--trending-instagram-reels-music--delosound.mp3",
        "punchy--hip-hop-beat--themountain.mp3",
    ],
    "curious": [
        "curious--mysterious-fog-curious-discovery--alex-morgan.mp3",
        "curious--curious-circuits--sonican.mp3",
        "curious--inquisitive-curiosity--musictown.mp3",
        "curious--mystery--soundpromusic.mp3",
        "curious--inquisitive-orchestra--musictown.mp3",
    ],
    "lofi": [
        "lofi--chill-lofi--zephiramusic.mp3",
        "lofi--lofi-chill--zephiramusic.mp3",
        "lofi--chill-lofi--velariomusic.mp3",
        "lofi--lofi-night-haze--ornave.mp3",
        "lofi--study-music--velariomusic.mp3",
        "lofi--chill-beats--atlasaudio.mp3",
    ],
    "confident": [
        "confident--technology-corporate--themountain.mp3",
        "confident--technology-music--nastelbom.mp3",
        "confident--tech-innovation--themountain.mp3",
        "confident--tech--atlasaudio.mp3",
        "confident--innovation--atlasaudio.mp3",
        "confident--abstract-technology--verclubmusic.mp3",
        "confident--tech-corporate--themountain.mp3",
    ],
    "bright": [
        "bright--upbeat-music--nastelbom.mp3",
        "bright--upbeat--subclair.mp3",
        "bright--feel-good-music--paulyudin.mp3",
        "bright--feel-good-music--starostin.mp3",
        "bright--feel-good-beat--tunetank.mp3",
    ],
    "cinematic": [
        "cinematic--cinematic-dramatic--atlasaudio.mp3",
        "cinematic--dramatic--themountain.mp3",
        "cinematic--dramatic--prettyjohn1.mp3",
        "cinematic--epic-trailer--nastelbom.mp3",
        "cinematic--epic-trailer-2--nastelbom.mp3",
    ],
    "minimal": [
        "minimal--ambient--nastelbom.mp3",
        "minimal--minimal-piano--leberch.mp3",
        "minimal--minimal-ambient-background--audiodollar.mp3",
        "minimal--minimal-minimalist--solarflex.mp3",
        "minimal--ambient-soft--avelinemusic.mp3",
        "minimal--instrumental-minimal--themountain.mp3",
    ],
    "triumphant": [
        "triumphant--triumphant--kulakovka.mp3",
        "triumphant--triumph-triumphant-fanfare--mfcc.mp3",
        "triumphant--victory-news-orchestral-anthem--sonican.mp3",
        "triumphant--success-music--paulyudin.mp3",
        "triumphant--success--themountain.mp3",
        "triumphant--great-achievement--themountain.mp3",
        "triumphant--motivational-uplifting-success--denis-pavlov-music.mp3",
    ],
}

MOODS = {
    "neutral":     ["confident-corporate-story--echoes-of-lumen.mp3"],
    "corporate":   ["confident-corporate-story--echoes-of-lumen.mp3"],
    # "confident" is literally in this track's own filename and MANIFEST.md's suggested
    # mood for it — missing here meant produce.sh's mood='confident' (episodes 32 and 33)
    # silently fell back to synthesized music instead of this real track, which is
    # exactly the "not what I sent you" complaint David raised after hearing episode 33.
    "confident":   ["confident-corporate-story--echoes-of-lumen.mp3"] + NEW["confident"],
    "urgent":      ["tense-suspense-rising-dread--alexmorgan.mp3"] + NEW["tense"],
    "triumphant":  ["success--paulyudin.mp3"] + NEW["triumphant"],
    "bright":      [
        "upbeat-and-inspiring--atlasaudio.mp3",
        "upbeat-energetic--maksymmalko.mp3",
        "energetic--atlasaudio-2.mp3",
        "upbeat-energetic--lnplusmusic.mp3",
        "energetic--ikoliksaj.mp3",
        "upbeat-energetic--ikoliksaj-2.mp3",
    ] + NEW["bright"],
    "lofi":        ["vibraphone--alexmorgan.mp3"] + NEW["lofi"],
    "retro":       ["nostalgic-memories-piano--alexmorgan.mp3"],
    "drive":       ["video-editing--alexmorgan.mp3"],
    "punchy":      ["trending-vibe--alexmorgan.mp3"] + NEW["punchy"],
    # New 16.9.2026 — a genuinely new mood, not a relabeling of an existing one.
    "scary":       ["scary-horror--arpmedia.mp3"],
    "horror":      ["scary-horror--arpmedia.mp3"],
    # tense-suspense-rising-dread, not suspense-tension-building: the latter opens on a
    # ~5s near-silent fade-in (measured -25 to -52 dB) that a straight from-0 trim landed
    # right on top of episode 27's hook, the one moment a quiet music bed can't afford to
    # be inaudible. alexmorgan's track is present from t=0 (measured -4 to -12 dB
    # throughout, no dead zone) and its dynamic range (17.9 dB) is much closer to
    # episode 26's upbeat-and-inspiring--atlasaudio.mp3 (15.4 dB) — the track David
    # pointed to as "sounds perfect" — than arpmedia's 33.2 dB swings.
    #
    # "tense" used to point at arpmedia separately from "suspense" — same failure mode,
    # different mood key. Episode 29 used "tense" and drew the same "no background
    # music" complaint a second time, even though every automated measurement of that
    # render (mean level, peak, integrated LUFS) came back healthy: the track is
    # technically present but reads as thin/absent to the ear, which measurement alone
    # doesn't catch (see audio/check_music_bed.py). Rather than maintain two mood keys
    # that both need the same fix, "tense" now points at the same alexmorgan track as
    # "suspense" — one fewer place for this exact bug to recur.
    "tense":       ["tense-suspense-rising-dread--alexmorgan.mp3"] + NEW["tense"],
    "suspense":    ["tense-suspense-rising-dread--alexmorgan.mp3"] + NEW["tense"],
    # New moods, 16.10.2026
    "curious":     NEW["curious"],
    "mystery":     NEW["curious"],
    "cinematic":   NEW["cinematic"],
    "dramatic":    NEW["cinematic"],
    "minimal":     NEW["minimal"],
    "ambient":     NEW["minimal"],
    "tech":        NEW["confident"],
    "upbeat":      NEW["bright"],
}


def load_history(path: str = HISTORY) -> list:
    try:
        with open(path) as f:
            h = json.load(f)
        return [x for x in h if isinstance(x, str)][-HISTORY_KEEP:]
    except (OSError, ValueError):
        return []


def save_history(history: list, path: str = HISTORY) -> None:
    with open(path, "w") as f:
        json.dump(history[-HISTORY_KEEP:], f, indent=1)


def choose(candidates: list, history: list) -> str:
    """Random pick that skips the last NO_REPEAT used tracks (when there is a choice)."""
    uniq = list(dict.fromkeys(candidates))
    if len(uniq) > 1:
        recent = set(history[-NO_REPEAT:])
        fresh = [c for c in uniq if c not in recent]
        if fresh:
            return random.choice(fresh)
    return random.choice(uniq)


def rotation_test(mood: str, runs: int = 10) -> None:
    """Simulate `runs` consecutive episodes on a mood, starting from the real history,
    without writing anything or cutting audio. Prints the distribution."""
    history = load_history()
    picks = []
    for _ in range(runs):
        c = choose(MOODS[mood], history)
        picks.append(c)
        history = (history + [c])[-HISTORY_KEEP:]
    for i, c in enumerate(picks, 1):
        print(f"{i:2d}. {c}")
    print(f"\ndistribution over {runs} runs for '{mood}' ({len(set(MOODS[mood]))} candidates):")
    for c, n in collections.Counter(picks).most_common():
        print(f"  {n}x {c}")
    bad = [i + 1 for i in range(len(picks)) if picks[i] in picks[max(0, i - NO_REPEAT):i]]
    print("repeat within the 3 previous picks:", bad or "none")


def probe_duration(path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(out)


def find_audible_start(path: str, src_dur: float, total: float, max_skip: float = 8.0) -> float:
    """Where to start the cut so it doesn't land on a quiet intro. A track like
    suspense-tension-building--arpmedia.mp3 opens on a several-second near-silent
    fade-in (measured -25 to -52 dB) — trimming from 0 put that dead zone right under
    episode 27's hook. Finds the first point ffmpeg's silencedetect calls "loud enough"
    (-24dB) and starts there instead, capped so a track that's genuinely a slow build
    throughout doesn't get skipped past its own intended intro, and so there's always
    enough source left to cover `total`."""
    cap = min(max_skip, max(0.0, src_dur - total))
    if cap <= 0:
        return 0.0
    out = subprocess.run(
        ["ffmpeg", "-v", "error", "-t", str(cap + 2), "-i", path,
         "-af", "silencedetect=noise=-24dB:d=0.3", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    for line in out.splitlines():
        if "silence_end" in line:
            # "silence_end: 4.83124 | silence_duration: ..." — the loud point right
            # after the intro's initial silence, if any is found this early.
            try:
                return min(cap, float(line.split("silence_end:")[1].split("|")[0].strip()))
            except (IndexError, ValueError):
                pass
    return 0.0


def main():
    if "--rotation-test" in sys.argv:
        mood = sys.argv[sys.argv.index("--rotation-test") + 1]
        if mood not in MOODS:
            sys.exit(f"unknown mood '{mood}'")
        rotation_test(mood)
        return
    total = float(sys.argv[1])
    out = sys.argv[2]
    mood = sys.argv[sys.argv.index("--mood") + 1] if "--mood" in sys.argv else "neutral"
    if mood not in MOODS:
        sys.exit(f"no real track mapped for mood '{mood}' — pick one of: {', '.join(sorted(MOODS))}")

    history = load_history()
    choice = choose(MOODS[mood], history)
    src = os.path.join(LIB, choice)
    if not os.path.exists(src):
        sys.exit(f"missing track file: {src}")

    src_dur = probe_duration(src)
    fade_in, fade_out = 0.3, 2.0
    fade_out_start = max(0.0, total - fade_out)

    filt = f"afade=t=in:st=0:d={fade_in},afade=t=out:st={fade_out_start}:d={fade_out}"
    cmd = ["ffmpeg", "-y", "-v", "error"]
    if src_dur < total:
        # loop the short clip enough times to cover the requested length
        cmd += ["-stream_loop", "-1", "-i", src, "-t", str(total)]
    else:
        start = find_audible_start(src, src_dur, total)
        cmd += (["-ss", str(start)] if start > 0 else []) + ["-i", src, "-t", str(total)]
    cmd += ["-ac", "1", "-ar", "48000", "-af", filt, out]
    subprocess.run(cmd, check=True)
    if "--no-record" not in sys.argv:
        save_history(history + [choice])
    print(f"wrote {out}  {total:.1f}s  mood={mood}  source={choice}")


if __name__ == "__main__":
    main()
