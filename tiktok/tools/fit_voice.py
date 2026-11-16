# Passt eine hochgeladene Sprecher-Aufnahme (z.B. ElevenLabs Brian) an: erkennt Satzteile über Pausen,
# kürzt lange Pausen und (optional) beschleunigt leicht. Gibt die neuen Startzeiten jedes Satzteils aus.
# Usage: python3 fit_voice.py <in.mp3> <out.wav> <times.json> --lines 0,2,7,13,19,23 [--gap 0.16] [--gap-line 0.30] [--tempo 1.0]
#   --lines: Indizes der Satzteile, mit denen eine neue Sprecherzeile (= neue Szene) beginnt
import subprocess, re, json, argparse
ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out"); ap.add_argument("times")
ap.add_argument("--lines", required=True); ap.add_argument("--gap", type=float, default=0.16)
ap.add_argument("--gap-line", type=float, default=0.30); ap.add_argument("--tempo", type=float, default=1.0)
ap.add_argument("--min-silence", type=float, default=0.18)
a = ap.parse_args()
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.inp], capture_output=True, text=True).stdout)
log = subprocess.run(["ffmpeg", "-i", a.inp, "-af", f"silencedetect=n=-40dB:d={a.min_silence}", "-f", "null", "-"], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]; en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
segs, cur = [], 0.0
for s, e in zip(st, en):
    if s > cur + 0.05: segs.append((cur, s))
    cur = e
if cur < dur - 0.05: segs.append((cur, dur))
line_start = {int(x) for x in a.lines.split(",")}
PAD = 0.04; t = 0.1; starts = []; flt = []
for i, (s0, s1) in enumerate(segs):
    if i > 0: t += a.gap_line if i in line_start else a.gap
    s2, e2 = max(0, s0 - PAD), min(dur, s1 + PAD)
    starts.append(t + (s0 - s2))
    flt.append(f"[0:a]atrim={s2:.3f}:{e2:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={e2-s2-0.03:.3f}:d=0.03,adelay={int(t*1000)}|{int(t*1000)}[s{i}]")
    t += e2 - s2
flt.append("".join(f"[s{i}]" for i in range(len(segs))) + f"amix=inputs={len(segs)}:normalize=0" + (f",atempo={a.tempo}" if a.tempo != 1.0 else "") + "[o]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.inp, "-filter_complex", ";".join(flt), "-map", "[o]", "-ar", "44100", a.out], check=True)
res = {"segments": [[round(s0, 2), round(s1, 2)] for s0, s1 in segs], "starts": [round(x / a.tempo, 3) for x in starts], "end": round(t / a.tempo, 3)}
json.dump(res, open(a.times, "w"), indent=1)
for i, (sg, s) in enumerate(zip(segs, res["starts"])): print(f"{i:2d} {'*' if i in line_start else ' '} orig {sg[0]:6.2f}-{sg[1]:6.2f}  neu {s:6.2f}")
print("Sprachende neu:", res["end"])
