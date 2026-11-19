# gen_cb_default.py: Chatterbox (MIT) with its BUILT-IN conds.pt voice (no reference clip, no cloning by us)
import torch, subprocess, torchaudio, soundfile as sf
from chatterbox.tts import ChatterboxTTS
torch.set_num_threads(8)
m = ChatterboxTTS.from_pretrained(device='cpu')
T = ["You talk. Ivy drafts the email. Done.", "ChatGPT knows your whole life. Your next AI shouldn't start from zero."]
for n, t in enumerate(T, 1):
    torch.manual_seed(7)
    w = m.generate(t, exaggeration=0.75, cfg_weight=0.3)
    torchaudio.save(f'/tmp/c{n}.wav', w, m.sr)
    subprocess.run(['ffmpeg','-y','-v','error','-i',f'/tmp/c{n}.wav','-ar','48000','-ac','1',f'ivy-chatterbox-default-L{n}.wav']); print(n, w.shape[1]/m.sr)
