# Produktions-Anleitung (für jede neue Folge)

Format: TikTok 1080×1920, 30 fps, **30–40 s**, Deutsch. Ordner pro Folge: `tiktok/<slug>/`.

## Aufbau jeder Folge (bewährt aus Teil 1 + 2)
1. **Hook (0–3 s):** Frage „WAS WÄRE, WENN …?" Wort für Wort, Schlüsselwort farbig.
2. **4 Zeitsprünge** mit Titel-Stempel („NACH 1 TAG" …), Fortschrittsleiste oben, rotem Zähler, 2 Fakt-Karten pro Szene (Karaoke-Text, *Schlüsselwort* gelb).
3. **Outro (~4 s):** Frage an Zuschauer + „Schreib's in die Kommentare" + „Folge für Teil N+1".
4. Visuell: eine durchgehende, animierte Welt, die sich verändert; Flash + Zoom-Punch + Shake an jedem Schnitt; großer Story-Moment pro Szene.
5. Text-Sicherheitszonen: nichts Wichtiges rechts > x 950 und unten > y 1500 (TikTok-Buttons/Caption).
6. Fakten müssen stimmen (populärwissenschaftlicher Konsens), keine erfundenen Zahlen.

## Ton
- **Erzähler (bevorzugt): ElevenLabs „Brian – Deep, Resonant and Comforting", Modell eleven v4, Deutsch.** Der Nutzer erzeugt die MP3 selbst in der ElevenLabs-App aus dem Sprechertext und lädt sie hoch. Dann: Pausen mit `ffmpeg -af silencedetect=n=-40dB:d=0.25` messen, Sätze zuordnen, Schnitte (`B`) auf den Beginn von „Nach …" legen (≈0,1 s davor), Story-Momente auf die passenden Wörter, und `tools/extvoice.sh <mp3> voice.wav` statt `voice.py` verwenden. Beispiel: `menschen-verschwinden/` (VIDEO_BOUNDS mit Extra-Stützpunkt für den Verschwinde-Moment).
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
