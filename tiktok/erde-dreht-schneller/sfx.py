# Soundeffekte "Erde dreht doppelt so schnell" – nur klar erkennbare Effekte (Regel aus ANLEITUNG.md)
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
B = [0, 3.4, 9.2, 15.4, 22.7, 29.8, 35.0]
SPEEDUP, STORM, RING, DAY_P = 1.65, 12.5, 26.6, 2.6
MIGRATE = (16.3, 21.6)
LIGHTNING = [11.2, 13.3, 14.5]
VOLC = B[4] + 1.6
tr = Track(B[-1])

# Hook: Erde dreht hoch – aufheulender "Turbinen"-Ton + Whoosh
d = 1.4; tt = T(d)
spin = chirp(110, 330, d, 1.5) * (0.4 + 0.6 * tt / d) + 0.4 * chirp(220, 660, d, 1.5) * (tt / d)
tr.add(SPEEDUP - 0.2, fade(spin, 0.2, 0.4), 0.22)
whoosh_in(tr, SPEEDUP + 0.25, 0.8, 0.4)
sub_drop(tr, SPEEDUP + 0.25, 0.4, 1.0)
whoosh_in(tr, B[1], 0.9, 0.3)
# Zeitraffer: Uhr tickt schnell, jeder Sonnenaufgang mit leisem "Swish"
tick_fast(tr, B[1] + 0.3, B[3] - 0.2, 8, 8, 0.18)
k = B[1] + ((0.0 - 0.18) % 1) * DAY_P
while k < B[3]:
    if k > B[1]: tr.add(k, filt(noise(0.5), 1500, 7000) * np.hanning(int(0.5 * SR)), 0.12, 0.3)
    k += DAY_P
# Sturm: Regen (sichtbar), Donner zu jedem Blitz
d = B[3] - (STORM - 1.5)
tr.add(STORM - 1.5, fade(stereo(filt(noise(d), 2500, 9000), 0.03), 1.2, 0.4), 0.16)
for lt in LIGHTNING:
    tr.add(lt, np.pad(filt(noise(0.12), 1500, 9000) * np.exp(-T(0.12) * 25), (0, 0)), 0.5)
    dd = 2.4; th = filt(noise(dd), hi=300) * np.exp(-T(dd) * 1.6) * (1 + 0.6 * np.sin(2 * np.pi * 3 * T(dd)))
    tr.add(lt + 0.15, reverb(th, 1.5, 0.4), 0.8)
# Meere strömen zum Äquator: mächtiges Wasserrauschen + Wellen
d = MIGRATE[1] - MIGRATE[0] + 1.0
wave_ = filt(noise(d), 200, 2500) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 0.6 * T(d))))
tr.add(MIGRATE[0], fade(stereo(wave_, 0.04), 1.0, 1.2), 0.32)
bubbles(tr, MIGRATE[0], MIGRATE[1], 25, 0.08)
# Vulkane: Explosionen, Erdbeben-Stöße
for i, t0 in enumerate([VOLC, VOLC + 0.9, VOLC + 2.1, VOLC + 3.3]):
    boom(tr, t0, 0.55 - i * 0.06, 2.0)
    tr.add(t0 + 0.05, filt(noise(0.6), 800, 5000) * np.exp(-T(0.6) * 6), 0.2, [0.3, 0.7, 0.45, 0.6][i])
# Ozean-Gürtel schließt sich: Whoosh + Glocke
whoosh_in(tr, RING + 0.6, 1.2, 0.35); ding(tr, RING + 0.6, 0.2)
# UI-Pops
facts = [(B[1], 1.2), (B[1], 3.0), (B[2], 1.0), (B[2], STORM - B[2] + 0.1), (B[3], 1.0), (B[3], 3.8), (B[4], 1.0), (B[4], RING - B[4] + 0.2)]
for a, f in facts: pop(tr, a + f)
for x in (0.1, 0.28, 0.46, 0.64, 0.82): pop(tr, B[5] + x, 0.2)
ding(tr, B[5] + 1.3)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
