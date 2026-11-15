# Soundeffekte Teil 2 – Video-Zeiten passend zu scene.html
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
B = [0, 3.0, 10.2, 15.0, 23.0, 31.3, 35.5]
DARK, MOONOFF, DIVE, ZOOMOUT = 7.8, 9.05, 19.15, 28.4
tr = Track(B[-1])

# Hook: Sommer – Vögel, leichter Wind, Herzschlag baut Spannung auf
wind(tr, 0, DARK, 0.10, 300, 1500)
for _ in range(10): bird(tr, rng.uniform(0.1, DARK - 0.4), rng.uniform(0.15, 0.85))
heartbeat(tr, 0.4, B[1], 80, 0.45)
whoosh_in(tr, B[1], 0.9, 0.3)
# 8 Minuten: schneller werdendes Ticken bis zur Dunkelheit, dann absolute Stille + Einschlag
tick_fast(tr, B[1] + 0.2, DARK - 0.05, 4, 16, 0.3)
whoosh_in(tr, DARK, 1.6, 0.45)
boom(tr, DARK, 0.9)
sub_drop(tr, DARK, 0.6, 2.0)
# Mond erlischt: kurzes "Glas-Ausklingen"
tr.add(MOONOFF, (np.sin(2 * np.pi * 1760 * T(1.5)) + 0.5 * np.sin(2 * np.pi * 2640 * T(1.5))) * np.exp(-T(1.5) * 3), 0.12, 0.2)
crickets(tr, MOONOFF, B[2], 0.04)
# 1 Woche: eisiger, heulender Wind, Frost knistert
wind(tr, B[2], B[4], 0.30, 250, 2000, howl=True)
for _ in range(40):
    tr.add(rng.uniform(B[2] + 0.5, B[4]), filt(noise(0.03), 3000, 12000) * np.exp(-T(0.03) * 100), rng.uniform(0.05, 0.15), rng.uniform(0.1, 0.9))
# 1 Jahr: Meer friert – tiefes Eis-Knacken; dann Abtauchen
for t0, p in [(B[3] + 1.6, 0.3), (B[3] + 2.7, 0.7), (B[3] + 3.4, 0.5)]: ice_crack(tr, t0, 0.55, p)
tr.add(DIVE - 0.1, filt(noise(0.8), 200, 3000) * np.exp(-T(0.8) * 4), 0.5)   # Eintauchen
underwater(tr, DIVE, B[4], 0.55)
bubbles(tr, DIVE, B[4], 45, 0.14)
tr.add(DIVE + 0.6, fade(filt(noise(B[4] - DIVE - 0.6), 60, 400) * 1.5, 0.8, 0.3), 0.25)   # Rumoren des Schlots
# 1 Mio Jahre: Stille, nur tiefer Drone + leises Rieseln (gefrorene Luft)
tr.add(B[4], fade(filt(noise(B[5] - B[4]), 4000, 12000) * 0.3, 1.0, 1.0), 0.12)
whoosh_in(tr, ZOOMOUT + 0.5, 1.4, 0.4)
d = B[-1] - ZOOMOUT; tr.add(ZOOMOUT, fade(np.sin(2 * np.pi * 55 * T(d)) + 0.5 * np.sin(2 * np.pi * 82.5 * T(d)), 1.5, 1.5), 0.25)
# UI-Pops bei Texteinblendungen
facts = [(B[1], 1.2), (B[1], DARK - B[1] - 0.2), (B[2], 0.9), (B[2], 2.7), (B[3], 1.0), (B[3], DIVE - B[3] + 0.2), (B[4], 1.0), (B[4], ZOOMOUT - B[4] + 0.3)]
for a, f in facts: pop(tr, a + f)
for x in (0.1, 0.4, 0.58, 0.76): pop(tr, B[5] + x, 0.2)
ding(tr, B[5] + 1.4)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
