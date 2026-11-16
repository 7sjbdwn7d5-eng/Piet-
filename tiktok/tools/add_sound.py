# Nimmt ein hochgeladenes Geräusch in die Bibliothek auf: Stille vorne/hinten abschneiden, Lautstärke angleichen,
# als MP3 in tiktok/sounds/<kategorie>/<name>.mp3 speichern und in sounds/index.json + sounds/README.md eintragen.
# Usage: python3 add_sound.py <datei> <name> <kategorie> "<Beschreibung>" "<passt zu, Komma-getrennt>" "<Quelle/Lizenz>"
import subprocess, json, os, sys
src, name, cat, desc, tags, source = sys.argv[1:7]
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sounds')
os.makedirs(os.path.join(base, cat), exist_ok=True)
out = os.path.join(base, cat, name + '.mp3')
af = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,"
      "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
      "loudnorm=I=-16:TP=-1.5,afade=t=out:st=0:d=0")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", af.replace(",afade=t=out:st=0:d=0", ""), "-ar", "44100", "-ac", "2", "-b:a", "192k", out], check=True)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
idx_p = os.path.join(base, 'index.json')
idx = json.load(open(idx_p)) if os.path.exists(idx_p) else {}
idx[name] = {"datei": f"{cat}/{name}.mp3", "kategorie": cat, "beschreibung": desc, "passt_zu": [t.strip() for t in tags.split(',') if t.strip()], "dauer_s": round(dur, 2), "quelle": source}
json.dump(idx, open(idx_p, 'w'), ensure_ascii=False, indent=1)
rows = "\n".join(f"| `{k}` | {v['kategorie']} | {v['beschreibung']} | {', '.join(v['passt_zu'])} | {v['dauer_s']} s | {v['quelle']} |" for k, v in sorted(idx.items(), key=lambda kv: (kv[1]['kategorie'], kv[0])))
open(os.path.join(base, 'README.md'), 'w').write(
"# Geräusche-Bibliothek\n\nVom Nutzer bereitgestellte echte Geräusche. **Vor dem Bauen jedes Videos hier nachsehen** und passende Geräusche "
"mit `sample(\"name\")` aus `tools/sfxlib.py` statt synthetischer Effekte verwenden.\n\n"
"| Name | Kategorie | Beschreibung | Passt zu | Dauer | Quelle/Lizenz |\n|---|---|---|---|---|---|\n" + rows + "\n")
print("aufgenommen:", name, f"({dur:.2f} s) ->", out)
