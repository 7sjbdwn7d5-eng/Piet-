# Der Zuschauer-Effekt (Gleichnis-Format, echtes Experiment)

~39 s, 9:16. Teil 1: dunkler Lampen-Raum (Rauch-Experiment). Teil 2 ab „Dumme Leute, denkst du?": schwarz, Strichmännchen, gelber Helfer.

## Quellenlage
- Latané & Darley (1968), „Group inhibition of bystander intervention in emergencies", *J. of Personality and Social Psychology* 10(3): Rauch strömt durch ein Lüftungsgitter in einen Raum, in dem Studierende einen Fragebogen ausfüllen.
  - Allein: 75 % melden den Rauch.
  - Mit zwei passiven Eingeweihten: nur 10 % (1 von 10).
- 112 = europaweite Notrufnummer. Der Tipp, eine Person direkt anzusprechen, ist eine gängige Erste-Hilfe-Empfehlung gegen Verantwortungsdiffusion.
- Die Straßenszene in Teil 2 ist eine Veranschaulichung, kein dokumentierter Einzelfall.

## Sprechertext (für ElevenLabs)
```
Ein echtes Experiment. Du sitzt allein in einem Raum und füllst einen Fragebogen aus.
Plötzlich quillt Rauch aus der Wand. Drei von vier stehen sofort auf und melden es.
Jetzt dasselbe. Aber neben dir sitzen zwei Fremde. Sie tun so, als wäre nichts.
Der Raum füllt sich mit Rauch. Nur einer von zehn steht auf.
Dumme Leute, denkst du? Auf der Straße bricht jemand zusammen. Zwanzig Menschen schauen zu. Jeder denkt: Ein anderer hilft schon.
Der Trick: Sprich eine Person direkt an. Du mit der roten Jacke: Ruf eins eins zwei!
Wann hast du zuletzt gedacht: Das macht schon jemand anderes?
```

## Bauen
`voice.py --speed 1.0` (Platzhalter Thorsten) → `captions.py lines.json voice.wav captions.js 1` → `sfx.py` → `audio.py --bounds 0,5.41,10.73,16.58,20.13,28.4,33.6,38.9 --drop 20.13,21.68` → render → mix. Hochgeladene ElevenLabs-MP3 mit `fit_voice.py` einpassen.
