# TikTok: „Was wäre, wenn plötzlich alle Menschen verschwinden?"

**Video mit Sprecher (empfohlen):** `erde_ohne_menschen_sprecher.mp4` – 36,5 s, 1080×1920 (9:16), 30 fps, deutscher Sprecher + Soundtrack (Musik wird unter der Stimme automatisch leiser).

**Erste Fassung ohne Sprecher:** `erde_ohne_menschen.mp4` – 44 s.

## Ablauf (Zeiten der 44-s-Fassung; die Sprecher-Fassung ist pro Szene gestrafft: Schnitte bei 3,0 / 10,0 / 17,0 / 23,6 / 31,6 s)
| Zeit | Szene | Was passiert |
|---|---|---|
| 0–3,6 s | Hook | Text knallt Wort für Wort rein, Menschen lösen sich in Partikel auf |
| 3,6–12,2 s | **1 Tag** | Fenster & Straßenlaternen gehen flackernd aus, Autos bleiben stehen, Wasser quillt aus Gullis |
| 12,2–20,8 s | **1 Woche** | Kühlturm glüht rot (Warnsymbol), Hund streunt, Milchstraße erscheint |
| 20,8–29,8 s | **1 Jahr** | Tag, Risse in der Straße, Gras, Ranken an Häusern, Hirsche |
| 29,8–39,2 s | **100 Jahre** | Häuser stürzen ein, Wald, Vögel, Abendlicht |
| 39,2–44 s | Outro | Frage an Zuschauer → Kommentare + „Folge für Teil 2" |

Retention-Elemente: Fortschrittsleiste oben, tickender Zähler (Stunde/Tag/Monat/Jahr), Flash + Zoom-Punch + Bass-Schlag bei jedem Zeitsprung, Karaoke-Text mit gelben Schlüsselwörtern.

## Sprechertext (steckt in `voice.py`; Zeiten unten = alte 44-s-Fassung)
- **0 s:** Was wäre, wenn plötzlich alle Menschen verschwinden?
- **3,6 s:** Nach einem Tag: Die Kraftwerke fallen aus – die Lichter gehen aus. U-Bahn-Tunnel laufen voll Wasser.
- **12,2 s:** Nach einer Woche: Atomkraftwerke verlieren ihre Kühlung. Und ohne Lichtsmog leuchtet die Milchstraße.
- **20,8 s:** Nach einem Jahr: Pflanzen sprengen den Asphalt. Wilde Tiere erobern die Städte.
- **29,8 s:** Nach hundert Jahren: Die meisten Häuser sind eingestürzt. Was bleibt? Beton, Plastik – und die Pyramiden.
- **39,2 s:** Was glaubst du, überlebt am längsten? Schreib's in die Kommentare!

## Caption-Vorschlag
Was bleibt von uns übrig? 🌍⏳ #waswärewenn #erdeohnemenschen #wissen #fakten #lernenmittiktok #gedankenexperiment #fyp

## Neu rendern / anpassen
- Bildtexte: `SCENES` in `scene.html`; Szenenlängen im Video: `VIDEO_BOUNDS` (`scene.html`) und `B` (`audio.py`) – beide gleich halten.
- Gesprochener Text + Einsatzzeiten: `LINES` in `voice.py`.
- `scene.html` im Browser öffnen = Live-Vorschau.

```bash
pip install piper-tts
curl -L -o v.tar.gz https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-de-thorsten-low.tar.gz && tar xzf v.tar.gz
python3 voice.py de-thorsten-low.onnx voice.wav
python3 audio.py music.wav
node render.js video_noaudio.mp4
ffmpeg -i music.wav -i voice.wav -filter_complex "[1:a]apad=whole_dur=36.5[vp];[0:a]volume=0.55[m];[vp]asplit=2[v][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[md];[md][v]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]" -map "[a]" -t 36.5 mix.wav
ffmpeg -i video_noaudio.mp4 -i mix.wav -c:v copy -c:a aac -b:a 192k erde_ohne_menschen_sprecher.mp4
```
