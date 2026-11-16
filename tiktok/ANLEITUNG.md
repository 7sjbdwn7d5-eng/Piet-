# Produktions-Anleitung (für jede neue Folge)

Format: TikTok 1080×1920, 30 fps, **30–40 s**, Deutsch. Ordner pro Folge: `tiktok/<slug>/`.

## AKTUELLES FORMAT: Story (Vorlage: `pompeji/`) – Wunsch des Nutzers nach Vorbild-Video
- **Kleine Geschichte mit 1–2 erfundenen Figuren** (Name! z.B. Bäcker Marcus + Hund Felix) in einer **echten** Situation/Epoche.
  Präsens, kurze Sätze, Spannung, Gefühl; Ende = **Cliffhanger** („Schaffen es die beiden?" + „Teil 2 folgt").
- **Grafik:** flache Vektor-Illustration mit detailreichen Kulissen; Figuren mit runden Köpfen, großen Augen, Augenbrauen-Mimik
  (`face()` moods: calm/happy/worried/shock/sad), Schweißtropfen; Tier-Nahaufnahmen (`dogHead()`); Nahaufnahmen mit
  **unscharfem Hintergrund** (`blurred()` / `layer()` – NIE `ctx.filter` pro Bild verwenden, das macht das Rendern 30× langsamer), ständige Kamerafahrten (`camera()`), etwa alle 2 s eine neue Einstellung.
- **Untertitel:** `tools/captions.py` erzeugt aus lines.json (`[start, TTS-Text, UNTERTITEL mit *ROT*-Wörtern, pos]`) 2–3-Wort-Häppchen,
  Schrift **Anton** (`tiktok/fonts/`), weiß, wichtige/gefährliche Wörter rot; bei Gesichts-Nahaufnahmen oben (Liste `TOP` in scene.html).
- **REAL-Schild** oben links: grüne Pille „REAL" + echter Fakt (Quellen im README). Kein Zeitstrahl, keine Fakt-Kästen.
- Ton: nur klar erkennbare Effekte zu sichtbaren Ereignissen (Tierlaute, Kette, Knall, Herzschlag, Schritte …), am Ende Stille.

## Früheres Format: „Ein Tag als …" / „Die letzten Stunden von …" (Vorlage: `gladiator/`)
- Hook (≈4 s): „EIN TAG ALS [ROLLE]" + Ort/Epoche + „Würdest DU überleben?" mit Fahrt in die Welt hinein.
- 4 Uhrzeit-Szenen (z.B. 06:00 / 12:00 / 15:00 / 16:00 + Titel) statt Zeitsprüngen; Timeline-Knoten = Uhrzeiten; rote Pille = Ort.
- Pro Szene 2–5 Einstellungen mit Figuren (Funktion `gladiator()` als Beispiel für eine Figur mit Posen), Nahaufnahmen von Gegenständen, große Stempel/Zahlen, Wisch-Übergänge.
- Echte, überraschende Fakten (mit Quellenlage im README), Mythen aufklären.
- Outro: Entweder-oder-Frage passend zur Rolle („SCHWERT oder DREIZACK?").

## Aufbau (altes Format „Was wäre, wenn …?", bewährt aus Teil 1 + 2)
1. **Hook (0–3 s):** Frage „WAS WÄRE, WENN …?" Wort für Wort, Schlüsselwort farbig.
2. **4 Zeitsprünge** mit Titel-Stempel („NACH 1 TAG" …), Fortschrittsleiste oben, rotem Zähler, 2 Fakt-Karten pro Szene (Karaoke-Text, *Schlüsselwort* gelb).
3. **Outro (~4 s):** Frage an Zuschauer + „Schreib's in die Kommentare" + „Folge für Teil N+1".
4. Visuell: **viel Abwechslung** (Wunsch des Nutzers) – pro Szene 2–3 verschiedene Einstellungen (z.B. Landschaft → Nahaufnahme → Ansicht aus dem All → Split-Screen → Innenraum mit Figur), etwa alle 2–4 s ein neues Bild. Wechsel genau auf passende Wörter des Sprechers legen. Flash + Zoom-Punch an Szenenwechseln, Wisch-Übergang (`drawWipe`) zwischen Einstellungen. Vorlage: `erde-dreht-schneller/scene.html` (`drawShot`).
4b. Schlussfrage: zur Folge passend, möglichst Entweder-oder („Wo würdest DU leben: X oder Y?") oder persönlich („Was tust DU als Erstes?") – nicht jedes Mal dieselbe Frage.
5. Text-Sicherheitszonen: nichts Wichtiges rechts > x 950 und unten > y 1500 (TikTok-Buttons/Caption).
6. Fakten müssen stimmen (populärwissenschaftlicher Konsens), keine erfundenen Zahlen.

## Ton
- **Geräusche-Bibliothek `tiktok/sounds/` (echte Aufnahmen des Nutzers) hat Vorrang vor synthetischen Effekten.** Vor jedem Video `sounds/README.md` lesen und in sfx.py `snd(tr, t, "name", g, fallback=...)` verwenden, wo ein Geräusch zum Bild passt. Neue Uploads mit `python3 tools/add_sound.py <datei> <name> <kategorie> "<Beschreibung>" "<passt zu>" "<Quelle>"` aufnehmen (Name klein, mit Unterstrich, z.B. `hund_knurrt`).
- **Erzähler (bevorzugt): ElevenLabs „Brian – Deep, Resonant and Comforting", Modell eleven v4, Deutsch.** Der Nutzer erzeugt die MP3 selbst in der ElevenLabs-App aus dem Sprechertext und lädt sie hoch. Dann: Pausen mit `ffmpeg -af silencedetect=n=-40dB:d=0.25` messen, Sätze zuordnen, Schnitte (`B`) auf den Beginn von „Nach …" legen (≈0,1 s davor), Story-Momente auf die passenden Wörter, und `tools/extvoice.sh <mp3> voice.wav` statt `voice.py` verwenden. Beispiel: `menschen-verschwinden/` (VIDEO_BOUNDS mit Extra-Stützpunkt für den Verschwinde-Moment).
- Hochgeladene Aufnahme transkribieren (der Nutzer ändert Sätze manchmal selbst!): `ffmpeg -i in.mp3 -ac 1 -ar 16000 in.wav` und `python3 tools/stt.py ~/voices/sherpa-onnx-whisper-small in.wav "0-10,10-20,…"`. Geänderte Sätze im Bild (Fakt-Karten/Outro) übernehmen.
- Brian-Aufnahme einpassen: `python3 tools/fit_voice.py sprecher_brian.mp3 cut.wav fit.json --lines <Index je Zeilenanfang>` – erkennt Satzteile, kürzt Pausen (0,16 s / 0,30 s), optional `--tempo 1.03`. Danach Schnitte/Bildwechsel aus `fit.json` (starts) setzen und `tools/extvoice.sh cut.wav voice.wav` – Beispiel: `pyramidenbauer/`.
- Solange keine Brian-Aufnahme da ist: Ersatz-Erzähler Piper (siehe unten), und dem Nutzer den Sprechertext zum Einfügen in ElevenLabs schicken.
- **Erzähler:** Piper „Thorsten high" (`tools/voice.py`), Text + Einsatzzeiten in `<slug>/lines.json`. Erst Zeilen einsprechen, Längen messen, DANN Szenen-Schnitte (`B` in scene.html) danach legen. Jede Zeile muss vor dem nächsten Schnitt enden.
- **Hintergrund-Stimme** (Nachrichten/Durchsage/Funk, Piper „Kerstin"): `tools/news.py` mit `<slug>/news.json`; darf mitten im Satz abbrechen, wenn die Story es verlangt.
- **Musik:** `tools/audio.py --bounds … [--drop a,b]`.
- **Effekte:** `<slug>/sfx.py` nutzt `tools/sfxlib.py` (Wind, Vögel, Knacken, Boom, Ticken, Herzschlag, Blasen, Pops …).
- **Mix:** `tools/mix.sh` (Ducking unter dem Erzähler, ≈ −12 LUFS).

## Setup in einer frischen Umgebung
```bash
pip install piper-tts scipy
mkdir -p ~/voices && cd ~/voices
curl -L -o th.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-de_DE-thorsten-high.tar.bz2 && tar xjf th.tar.bz2
curl -L -o k.tar.gz https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-de-kerstin-low.tar.gz && tar xzf k.tar.gz
pip install sherpa-onnx   # Spracherkennung
curl -L -o ws.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2 && tar xjf ws.tar.bz2
```
Thorsten: `~/voices/vits-piper-de_DE-thorsten-high/de_DE-thorsten-high.onnx`, Kerstin: `~/voices/de-kerstin-low.onnx`.

## Bauen (Beispiel)
```bash
cd tiktok/tools
python3 voice.py ~/voices/vits-piper-de_DE-thorsten-high/de_DE-thorsten-high.onnx /tmp/voice.wav ../<slug>/lines.json
python3 news.py ~/voices/de-kerstin-low.onnx /tmp/news.wav ../<slug>/news.json
python3 audio.py /tmp/music.wav --bounds 0,3,…,ENDE [--drop a,b]
python3 ../<slug>/sfx.py /tmp/sfx.wav
node render.js ../<slug>/scene.html --stills 1.5,6,12,… /tmp/stills   # Kontrollbilder ansehen!
node render.js ../<slug>/scene.html /tmp/video.mp4
./mix.sh /tmp/music.wav /tmp/sfx.wav /tmp/news.wav /tmp/voice.wav /tmp/video.mp4 ../<slug>/<slug>_final.mp4
```
Am Ende: Thema in `THEMEN.md` abhaken, README im Ordner (Ablauf, Sprechertext, Caption + Hashtags), committen, pushen.

## Ton-Regeln (Wunsch des Nutzers)
- **Keine undeutlichen Hintergrundgeräusche:** keine Rausch-Teppiche (Stadt-/Verkehrslärm, Wind, Grollen, Brummen, Knistern, Flügelschlag), keine verzerrten/verrauschten Hintergrundstimmen (TV/PA/Funk mit Bitcrusher), keine Pfeiftöne.
- Erlaubt sind **klar erkennbare** Effekte, die zu einem sichtbaren Ereignis gehören (z.B. Wasser, Sirene, Geigerzähler, Explosion/Einsturz, Vögel, Übergangs-Whoosh, Pops). Hintergrund-Durchsagen nur klar verständlich (Filter `ALARM_CLEAR`).
