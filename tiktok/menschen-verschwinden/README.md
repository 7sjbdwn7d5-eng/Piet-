# TikTok: „Was wäre, wenn plötzlich alle Menschen verschwinden?"

**Video:** `erde_ohne_menschen.mp4` – 44 s, 1080×1920 (9:16), 30 fps, mit synthetisiertem Soundtrack.

## Ablauf
| Zeit | Szene | Was passiert |
|---|---|---|
| 0–3,6 s | Hook | Text knallt Wort für Wort rein, Menschen lösen sich in Partikel auf |
| 3,6–12,2 s | **1 Tag** | Fenster & Straßenlaternen gehen flackernd aus, Autos bleiben stehen, Wasser quillt aus Gullis |
| 12,2–20,8 s | **1 Woche** | Kühlturm glüht rot (Warnsymbol), Hund streunt, Milchstraße erscheint |
| 20,8–29,8 s | **1 Jahr** | Tag, Risse in der Straße, Gras, Ranken an Häusern, Hirsche |
| 29,8–39,2 s | **100 Jahre** | Häuser stürzen ein, Wald, Vögel, Abendlicht |
| 39,2–44 s | Outro | Frage an Zuschauer → Kommentare + „Folge für Teil 2" |

Retention-Elemente: Fortschrittsleiste oben, tickender Zähler (Stunde/Tag/Monat/Jahr), Flash + Zoom-Punch + Bass-Schlag bei jedem Zeitsprung, Karaoke-Text mit gelben Schlüsselwörtern.

## Sprechertext (optional, z. B. TikTok-„Text-zu-Sprache" oder eigene Stimme)
- **0 s:** Was wäre, wenn plötzlich alle Menschen verschwinden?
- **3,6 s:** Nach einem Tag: Die Kraftwerke fallen aus – die Lichter gehen aus. U-Bahn-Tunnel laufen voll Wasser.
- **12,2 s:** Nach einer Woche: Atomkraftwerke verlieren ihre Kühlung. Und ohne Lichtsmog leuchtet die Milchstraße.
- **20,8 s:** Nach einem Jahr: Pflanzen sprengen den Asphalt. Wilde Tiere erobern die Städte.
- **29,8 s:** Nach hundert Jahren: Die meisten Häuser sind eingestürzt. Was bleibt? Beton, Plastik – und die Pyramiden.
- **39,2 s:** Was glaubst du, überlebt am längsten? Schreib's in die Kommentare!

## Caption-Vorschlag
Was bleibt von uns übrig? 🌍⏳ #waswärewenn #erdeohnemenschen #wissen #fakten #lernenmittiktok #gedankenexperiment #fyp

## Neu rendern / anpassen
Texte & Zeiten stehen oben in `scene.html` (`S` und `SCENES`). `scene.html` im Browser öffnen = Live-Vorschau.
```bash
python3 audio.py soundtrack.wav
node render.js video_noaudio.mp4
ffmpeg -i video_noaudio.mp4 -i soundtrack.wav -c:v copy -c:a aac -b:a 192k -shortest erde_ohne_menschen.mp4
```
