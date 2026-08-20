"""His cloned voice, in Dutch and in Hebrew. The multilingual checkpoint covers 23
languages including nl and he — so the question of whether he can front a Dutch channel
is a business question, not a technical one. This is the proof."""
import os, subprocess, torch, torchaudio, warnings
warnings.filterwarnings("ignore")
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

REF = "audio/voice/profile/reference.wav"
LINES = [
    ("nl", "Iedereen zegt AI agent. Bijna niemand kan uitleggen waar de chatbot ophoudt."),
    ("nl", "Een chatbot antwoordt. Een agent handelt: hij plant de stappen zelf."),
    ("he", "כולם אומרים סוכן AI. כמעט אף אחד לא יודע להסביר איפה הצ'אטבוט נגמר."),
    ("en", "Everyone says agent. Almost nobody can say where the chatbot ends."),
]
torch.set_num_threads(os.cpu_count() or 4)
m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
os.makedirs("audio/voice/lang", exist_ok=True)
outs = []
for i, (lang, text) in enumerate(LINES):
    torch.manual_seed(7)
    wav = m.generate(text, language_id=lang, audio_prompt_path=REF,
                     exaggeration=0.45, cfg_weight=0.45, temperature=0.75)
    raw = f"/tmp/lang{i}.wav"; torchaudio.save(raw, wav, m.sr)
    out = f"audio/voice/lang/{i}-{lang}.wav"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",raw,
      "-af","highpass=f=75,deesser=i=0.14:m=0.5:f=0.35,"
            "acompressor=threshold=-20dB:ratio=2.2:attack=10:release=200:makeup=1.5,"
            "alimiter=limit=0.95,loudnorm=I=-17:TP=-1.5:LRA=10",
      "-ar","48000","-ac","1",out], check=True)
    outs.append(out); print("wrote", out, flush=True)

lst="/tmp/langlist.txt"
with open(lst,"w") as f:
    for o in outs: f.write(f"file '{os.path.abspath(o)}'\n")
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",lst,
                "-af","loudnorm=I=-16:TP=-1.5","-c:a","aac","-b:a","192k",
                "export/voice-dutch-hebrew-english.m4a"], check=True)
print("montage written", flush=True)
