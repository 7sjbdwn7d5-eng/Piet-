# Erzeugt die Sprecher-Spur mit Piper TTS (Stimme "Thorsten", Deutsch) und legt jede Zeile auf ihren Szenenstart.
# Stimme: https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-de-thorsten-low.tar.gz
# Usage: python3 voice.py <modell.onnx> <out.wav>
import subprocess, sys, os, tempfile
MODEL, OUT = sys.argv[1], sys.argv[2]
# (Startzeit im Video in s, Text) – Startzeiten passen zu VIDEO_BOUNDS in scene.html
LINES = [
    (0.15, "Was wäre, wenn plötzlich alle Menschen verschwinden?"),
    (3.15, "Nach einem Tag. Die Kraftwerke fallen aus. Die Lichter gehen aus. U-Bahn-Tunnel laufen voll Wasser."),
    (10.15, "Nach einer Woche. Atomkraftwerke verlieren ihre Kühlung. Und über der dunklen Stadt leuchtet die Milchstraße."),
    (17.15, "Nach einem Jahr. Pflanzen sprengen den Asphalt. Wilde Tiere erobern die Städte."),
    (23.75, "Nach hundert Jahren. Die meisten Häuser sind eingestürzt. Was bleibt? Beton, Plastik, und die Pyramiden."),
    (31.85, "Was glaubst du, überlebt am längsten? Schreib es in die Kommentare!"),
]
tmp = tempfile.mkdtemp()
inputs, filters = [], []
for i, (start, text) in enumerate(LINES):
    f = os.path.join(tmp, f"l{i}.wav")
    subprocess.run([sys.executable, "-m", "piper", "-m", MODEL, "--length-scale", "0.92", "--sentence-silence", "0.15", "-f", f],
                   input=text.encode(), check=True, stderr=subprocess.DEVNULL)
    inputs += ["-i", f]
    ms = int(start * 1000)
    # etwas tiefere, "dokumentarische" Stimme bei gleichem Tempo
    filters.append(f"[{i}:a]aresample=44100,asetrate=44100*0.94,aresample=44100,atempo=1.0638,adelay={ms}|{ms}[v{i}]")
mix = "".join(f"[v{i}]" for i in range(len(LINES)))
filters.append(f"{mix}amix=inputs={len(LINES)}:normalize=0,highpass=f=70,acompressor=threshold=-20dB:ratio=4:attack=5:release=120,"
               f"aecho=0.8:0.6:45|90:0.18|0.08,loudnorm=I=-15:TP=-1.5,pan=stereo|c0=c0|c1=c0[out]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filters), "-map", "[out]", "-ar", "44100", OUT], check=True)
print("wrote", OUT)
