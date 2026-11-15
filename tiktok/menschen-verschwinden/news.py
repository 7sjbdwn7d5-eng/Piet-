# Hintergrund-Stimme (Nachrichten / Durchsagen) mit Piper TTS, Stimme "Kerstin".
# Stimme: https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-de-kerstin-low.tar.gz
# Usage: python3 news.py <de-kerstin-low.onnx> <out.wav>
import subprocess, sys, os, tempfile
MODEL, OUT = sys.argv[1], sys.argv[2]
TV = "highpass=f=300,lowpass=f=3800,acrusher=bits=10:mix=0.25,aecho=0.8:0.5:25:0.3"
PA = "highpass=f=450,lowpass=f=3000,acrusher=bits=9:mix=0.3,aecho=0.8:0.75:280|560|900:0.45|0.3|0.18"
ALARM = "highpass=f=400,lowpass=f=3200,flanger=delay=2:depth=3:speed=6,acrusher=bits=8:mix=0.35,aecho=0.8:0.7:180|420:0.4|0.25"
# (Start s, Ende/Abbruch s, Text, Filter, Lautstärke)
LINES = [
    (0.00, 1.75, "Eilmeldung! Weltweit verschwinden Menschen spurlos. Wir schalten jetzt live nach", TV, 1.0),  # bricht ab, wenn alle verschwinden
    (3.55, 7.72, "Achtung, Achtung. Großflächiger Stromausfall. Bitte bewahren Sie Ruhe.", PA, 1.0),            # verstummt mit dem Stromausfall
    (10.65, 13.90, "Warnung. Reaktorkühlung ausgefallen. Notstrom erschöpft.", ALARM, 1.0),
    (14.10, 16.95, "Warnung. Reaktorkühlung ausgefallen.", ALARM, 0.9),
]
tmp = tempfile.mkdtemp(); inputs = []; fl = []
for i, (s, e, text, f, vol) in enumerate(LINES):
    p = os.path.join(tmp, f"n{i}.wav")
    subprocess.run([sys.executable, "-m", "piper", "-m", MODEL, "--length-scale", "0.85", "--sentence-silence", "0.1", "-f", p],
                   input=text.encode(), check=True, stderr=subprocess.DEVNULL)
    inputs += ["-i", p]; ms = int(s * 1000)
    fl.append(f"[{i}:a]aresample=44100,atrim=0:{e - s:.3f},afade=t=out:st={e - s - 0.02:.3f}:d=0.02,{f},volume={vol},adelay={ms}|{ms}[n{i}]")
fl.append("".join(f"[n{i}]" for i in range(len(LINES))) + f"amix=inputs={len(LINES)}:normalize=0,loudnorm=I=-18:TP=-2,pan=stereo|c0=0.8*c0|c1=c0[out]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(fl), "-map", "[out]", "-ar", "44100", OUT], check=True)
print("wrote", OUT)
