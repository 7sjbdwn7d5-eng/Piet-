# Soundeffekte "Erde dreht doppelt so schnell" – nur klar erkennbare Effekte (Regel aus ANLEITUNG.md)
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
B = [0, 3.65, 10.2, 17.4, 25.7, 33.8, 38.8]
SPEEDUP, STORM, RING, DAY_P = 1.7, 14.2, 30.65, 2.6
CAL, HURR, SPLIT, POLE, VOLC0, VOLC1 = 7.25, 15.6, 21.45, 23.3, 29.0, 30.5
MIGRATE = (18.8, 21.3)
LIGHTNING = [14.45, 15.15]
VOLC = VOLC0 + 0.05
tr = Track(B[-1])

# Hook: Erde dreht hoch – aufheulender "Turbinen"-Ton + Whoosh
d = 1.4; tt = T(d)
spin = chirp(110, 330, d, 1.5) * (0.4 + 0.6 * tt / d) + 0.4 * chirp(220, 660, d, 1.5) * (tt / d)
tr.add(SPEEDUP - 0.2, fade(spin, 0.2, 0.4), 0.22)
whoosh_in(tr, SPEEDUP + 0.25, 0.8, 0.4)
sub_drop(tr, SPEEDUP + 0.25, 0.4, 1.0)
whoosh_in(tr, B[1], 0.9, 0.3)
# Zeitraffer: Uhr tickt schnell, jeder Sonnenaufgang mit leisem "Swish"
tick_fast(tr, B[1] + 0.3, CAL - 0.1, 8, 8, 0.18)
tick_fast(tr, STORM, HURR - 0.1, 8, 8, 0.12)
k = B[1] + ((0.0 - 0.18) % 1) * DAY_P
while k < B[3]:
    if k > B[1]: tr.add(k, filt(noise(0.5), 1500, 7000) * np.hanning(int(0.5 * SR)), 0.12, 0.3)
    k += DAY_P
# Wisch-Übergänge zwischen Einstellungen
for w in [CAL, STORM, HURR, SPLIT, VOLC0, VOLC1]: whoosh_in(tr, w + 0.05, 0.45, 0.3)
# Kalender: Seiten flattern, Zähler läuft hoch (Klick-Sequenz)
for i in range(46): tr.add(CAL + i * 0.06, filt(noise(0.05), 1200, 6000) * np.exp(-T(0.05) * 60), 0.12, 0.3 + 0.4 * ((i * 7) % 10) / 10)
for i in range(30): tr.add(CAL + 0.3 + i * 0.053, np.sin(2 * np.pi * (900 + i * 25) * T(0.03)) * np.exp(-T(0.03) * 120), 0.10)
ding(tr, CAL + 1.9, 0.3)
# Schlafzimmer: Wecker klingelt in Schüben
for k0 in np.arange(B[2], STORM, 2 * np.pi / 2.5):
    st0 = k0 + np.arcsin(0.3) / 2.5
    d = (np.pi - 2 * np.arcsin(0.3)) / 2.5
    if st0 + d > STORM: d = STORM - st0
    if d <= 0.05: continue
    bell = np.sign(np.sin(2 * np.pi * 22 * T(d))) * 0.5 + 0.5
    tone = (np.sin(2 * np.pi * 2100 * T(d)) + 0.6 * np.sin(2 * np.pi * 3150 * T(d))) * bell
    tr.add(st0, fade(tone, 0.01, 0.03), 0.07, 0.75)
# Hurrikan: tiefes, drehendes Heulen (sichtbarer Wirbel)
d = B[3] - HURR; tt = T(d)
hw = filt(noise(d), 300, 1800) * (0.6 + 0.4 * np.sin(2 * np.pi * 2.5 * tt)) + 0.3 * np.sin(2 * np.pi * np.cumsum(380 + 120 * np.sin(2 * np.pi * 1.2 * tt)) / SR)
tr.add(HURR, fade(stereo(hw, 0.05), 0.2, 0.3), 0.25)
# Split: Wasser gurgelt in der Stadt, Schiff knarzt am Pol
bubbles(tr, SPLIT, POLE, 18, 0.1)
d = 1.0; tr.add(POLE + 0.6, fade(filt(np.sign(np.sin(2 * np.pi * 70 * T(d))) * (0.5 + 0.5 * np.sin(2 * np.pi * 3 * T(d))), 150, 900), 0.1, 0.3), 0.12, 0.7)
# Lava blubbert
for i in range(14): tr.add(VOLC0 + 0.1 + i * 0.09, chirp(120, 60, 0.12) * np.exp(-T(0.12) * 20), 0.25, 0.4 + 0.2 * (i % 3) / 2)
# Sturm: Regen (sichtbar), Donner zu jedem Blitz
d = HURR - STORM
tr.add(STORM, fade(stereo(filt(noise(d), 2500, 9000), 0.03), 1.2, 0.4), 0.16)
for lt in LIGHTNING:
    tr.add(lt, np.pad(filt(noise(0.12), 1500, 9000) * np.exp(-T(0.12) * 25), (0, 0)), 0.5)
    dd = 2.4; th = filt(noise(dd), hi=300) * np.exp(-T(dd) * 1.6) * (1 + 0.6 * np.sin(2 * np.pi * 3 * T(dd)))
    tr.add(lt + 0.15, reverb(th, 1.5, 0.4), 0.8)
# Meere strömen zum Äquator: mächtiges Wasserrauschen + Wellen
d = MIGRATE[1] - MIGRATE[0] + 1.0
wave_ = filt(noise(d), 200, 2500) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 0.6 * T(d))))
tr.add(MIGRATE[0], fade(stereo(wave_, 0.04), 1.0, 1.2), 0.32)
bubbles(tr, MIGRATE[0], SPLIT, 15, 0.08)
# Vulkane: Explosionen, Erdbeben-Stöße
for i, t0 in enumerate([VOLC, VOLC + 0.9, VOLC + 2.1, VOLC + 3.3]):
    boom(tr, t0, 0.55 - i * 0.06, 2.0)
    tr.add(t0 + 0.05, filt(noise(0.6), 800, 5000) * np.exp(-T(0.6) * 6), 0.2, [0.3, 0.7, 0.45, 0.6][i])
# Ozean-Gürtel schließt sich: Whoosh + Glocke
whoosh_in(tr, RING + 0.6, 1.2, 0.35); ding(tr, RING + 0.6, 0.2)
# UI-Pops
facts = [(B[1], 1.2), (B[1], CAL - B[1]), (B[2], 1.0), (B[2], STORM - B[2] + 0.1), (B[3], 1.35), (B[3], SPLIT - B[3] + 0.1), (B[4], 2.0), (B[4], RING - B[4] + 0.2)]
for a, f in facts: pop(tr, a + f)
for x in (0.1, 0.3, 0.5, 0.7): pop(tr, B[5] + x, 0.2)
ding(tr, B[5] + 1.3)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
