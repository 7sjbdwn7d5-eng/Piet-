# Erzeugt die Sprecher-Spur mit Piper TTS und legt jede Zeile auf ihren Einsatzpunkt.
# Empfohlene Stimme (hohe Qualität, 22 kHz) – erreichbar über GitHub:
#   https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-de_DE-thorsten-high.tar.bz2
# Usage: python3 voice.py <modell.onnx> <out.wav> [lines.json] [--speaker N] [--pitch 0.97] [--speed 1.0]
#   lines.json: [[startzeit_s, "Text"], ...]  (ohne Angabe: Zeilen von Teil 1 unten)
import subprocess, sys, os, tempfile, json, argparse

ap = argparse.ArgumentParser()
ap.add_argument("model"); ap.add_argument("out"); ap.add_argument("lines", nargs="?")
ap.add_argument("--speaker", type=int, default=None)
ap.add_argument("--pitch", type=float, default=0.97, help="<1 = etwas tiefer")
ap.add_argument("--speed", type=float, default=1.0, help="Piper length-scale (>1 = langsamer)")
a = ap.parse_args()

LINES = [
    (0.15, "Was wäre, wenn plötzlich alle Menschen verschwinden?"),
    (3.15, "Nach einem Tag. Die Kraftwerke fallen aus. Die Lichter gehen aus. U-Bahn-Tunnel laufen voll Wasser."),
    (10.15, "Nach einer Woche. Atomkraftwerke verlieren ihre Kühlung. Und über der dunklen Stadt leuchtet die Milchstraße."),
    (17.15, "Nach einem Jahr. Pflanzen sprengen den Asphalt. Wilde Tiere erobern die Städte."),
    (23.75, "Nach hundert Jahren. Die meisten Häuser sind eingestürzt. Was bleibt? Beton, Plastik, und die Pyramiden."),
    (31.85, "Was glaubst du, überlebt am längsten? Schreib es in die Kommentare!"),
]
if a.lines:
    LINES = [tuple(x) for x in json.load(open(a.lines))]

tmp = tempfile.mkdtemp()
inputs, filters = [], []
for i, (start, text) in enumerate(LINES):
    f = os.path.join(tmp, f"l{i}.wav")
    cmd = [sys.executable, "-m", "piper", "-m", a.model, "--length-scale", str(a.speed), "--noise-scale", "0.6",
           "--noise-w", "0.7", "--sentence-silence", "0.22", "-f", f]
    if a.speaker is not None: cmd += ["-s", str(a.speaker)]
    subprocess.run(cmd, input=text.encode(), check=True, stderr=subprocess.DEVNULL)
    inputs += ["-i", f]
    ms = int(start * 1000)
    p = a.pitch
    filters.append(f"[{i}:a]aresample=48000,asetrate=48000*{p},aresample=48000,atempo={1 / p:.5f},adelay={ms}|{ms}[v{i}]")
mix = "".join(f"[v{i}]" for i in range(len(LINES)))
# warmer, weicher Klang: Tiefen leicht anheben, Härte/Zischlaute dämpfen, sanfte Kompression, kleiner Raum
filters.append(
    f"{mix}amix=inputs={len(LINES)}:normalize=0,highpass=f=75,"
    "equalizer=f=160:t=q:w=1:g=2.5,equalizer=f=3200:t=q:w=1.5:g=-1.5,deesser=i=0.4,"
    "acompressor=threshold=-22dB:ratio=2.5:attack=10:release=200:makeup=2,"
    "aecho=0.85:0.5:22|37:0.12|0.08,loudnorm=I=-15:TP=-1.5,pan=stereo|c0=c0|c1=c0[out]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filters), "-map", "[out]", "-ar", "44100", a.out], check=True)
print("wrote", a.out)
