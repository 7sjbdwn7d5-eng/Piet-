# Erzeugt 2–3-Wort-Untertitel (captions.js) aus Sprechertext + fertiger Sprachspur.
# lines.json: [[start_s, "TTS-Text", "UNTERTITEL MIT *ROT* MARKIERTEN WÖRTERN", "bottom"|"top"], ...]
# Usage: python3 captions.py lines.json voice.wav captions.js [max_woerter]
import json, re, subprocess, sys
lines = json.load(open(sys.argv[1])); wav = sys.argv[2]; out = sys.argv[3]
MAXW = int(sys.argv[4]) if len(sys.argv) > 4 else 3   # max. Wörter pro Untertitel (1 = Wort für Wort)
log = subprocess.run(["ffmpeg", "-i", wav, "-af", "silencedetect=n=-33dB:d=0.1", "-f", "null", "-"], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]; en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav], capture_output=True, text=True).stdout)
speech, cur = [], 0.0
for s, e in zip(st, en):
    if s > cur + 0.04: speech.append((cur, s))
    cur = e
if cur < dur - 0.04: speech.append((cur, dur))
caps = []
for i, L in enumerate(lines):
    start, cap = L[0], L[2]; pos = L[3] if len(L) > 3 else "bottom"
    nxt = lines[i + 1][0] if i + 1 < len(lines) else dur + 1
    segs = [(max(s[0], start), min(s[1], nxt - 0.1)) for s in speech if s[1] > start + 0.05 and s[0] < nxt - 0.1]
    segs = [s for s in segs if s[1] - s[0] > 0.08]
    phrases = [p.strip() for p in re.findall(r"[^.,?!:]+[.,?!:]*", cap) if p.strip()]
    if not segs: continue
    if len(segs) == len(phrases): spans = segs
    else:   # proportional verteilen
        a, b = segs[0][0], segs[-1][1]; tot = sum(len(p) for p in phrases); spans = []; t = a
        for p in phrases: d = (b - a) * len(p) / tot; spans.append((t, t + d)); t += d
    for p, (a, b) in zip(phrases, spans):
        words = p.split(); chunks = []; j = 0
        while j < len(words):
            n = 3 if len(" ".join(words[j:j + 3]).replace("*", "")) <= 16 else 2
            if len(words) - j == 4: n = 2
            n = min(n, MAXW)
            chunks.append(words[j:j + n]); j += n
        tot = sum(len(" ".join(c)) for c in chunks); t = a
        for c in chunks:
            d = (b - a) * len(" ".join(c)) / tot
            caps.append([round(t, 3), round(t + d, 3), c, pos]); t += d
for k in range(len(caps) - 1):       # Lücken füllen: Untertitel bleibt bis zum nächsten stehen (max +0.5 s)
    caps[k][1] = round(min(caps[k + 1][0], caps[k][1] + 0.5), 3)
open(out, "w").write("setCaptions(" + json.dumps(caps, ensure_ascii=False) + ");\n")
print(len(caps), "Untertitel geschrieben ->", out)
