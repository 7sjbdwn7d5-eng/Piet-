# Soundeffekte "Ein Tag als Pyramidenbauer" – nur klar erkennbare Effekte
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
B = [0, 3.95, 11.58, 18.35, 25.4, 31.85, 37.5]
AGO, NOSLAVE, TEAMS, CARS = 1.8, 6.45, 9.25, 13.65
SLED, WATER, GLIDE = 15.15, 16.1, 17.1
BREAD, ONION, BEER, LITER, WAGE, TOMB = 19.5, 20.25, 21.0, 21.4, 24.0, 28.55
WIPES = [NOSLAVE, TEAMS, SLED, LITER, WAGE, TOMB]
tr = Track(B[-1])
def drum(t0, g=0.6, low=1.0):
    d = 0.7; tt = T(d); f = 50 + 80 * np.exp(-tt * 18)
    tr.add(t0, np.sin(2 * np.pi * np.cumsum(f * low) / SR) * np.exp(-tt * 5) + filt(noise(d), 100, 900) * np.exp(-tt * 30) * 0.4, g)
def clink(t0, f, g=0.15, pan=0.5):
    tr.add(t0, (np.sin(2 * np.pi * f * T(0.25)) + 0.5 * np.sin(2 * np.pi * f * 2.7 * T(0.25))) * np.exp(-T(0.25) * 18), g, pan)
def rattle(t0, d=0.6, g=0.12):   # Sistrum (altägyptische Rassel)
    k = t0
    while k < t0 + d: clink(k, 3200 + 400 * np.sin(k * 40), g, 0.6); k += 0.045
def stamp(t0, g=0.7): drum(t0, g, 0.7); tr.add(t0, filt(noise(0.08), 400, 3000) * np.exp(-T(0.08) * 40), 0.4)
def pour(t0, d, g=0.25):
    tt = T(d); s = filt(noise(d), 500, 3500) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * tt)); tr.add(t0, fade(s, 0.1, 0.2), g, 0.6); bubbles(tr, t0, t0 + d, int(d * 12), 0.1)
# Hook: Trommeln + Sistrum
drum(0.05, 0.8); drum(0.35, 0.8); rattle(0.6, 0.8); drum(AGO, 0.7); rattle(AGO + 0.1, 0.5)
whoosh_in(tr, B[1], 0.9, 0.3)
# 05:00: Sistrum zum Aufwachen, Stempel KEINE SKLAVEN, Ketten
rattle(B[1] + 0.4, 0.7, 0.1)
for i in range(6): clink(NOSLAVE + 0.05 + i * 0.05, 900 + i * 90, 0.12, 0.4)
stamp(NOSLAVE + 0.2); stamp(NOSLAVE + 0.45, 0.6); pop(tr, NOSLAVE + 1.4)
# Teams: Pinselstriche + Zieh-Rhythmus (Trommel im Takt)
for i in range(7): tr.add(TEAMS + 0.2 + i * 0.13, filt(noise(0.09), 1500, 6000) * np.hanning(int(0.09 * SR)), 0.12, 0.5)
for i in range(5): drum(TEAMS + 0.1 + i * 0.5, 0.35)
pop(tr, TEAMS + 0.9, 0.3)
# 08:00: schwerer Block, Waage knarzt, Autos poppen
drum(B[2] + 0.9, 0.6, 0.6); pop(tr, CARS, 0.3); pop(tr, CARS + 0.25, 0.3)
d = 0.8; tr.add(B[2] + 0.4, fade(filt(np.sign(np.sin(2 * np.pi * 60 * T(d))) * (0.5 + 0.5 * np.sin(2 * np.pi * 4 * T(d))), 150, 900), 0.1, 0.3), 0.08, 0.5)
# Schlitten: Zieh-Trommel, Wasser gießen, Gleiten
for i in range(int((B[3] - SLED) / 0.5)): drum(SLED + i * 0.5, 0.3 if SLED + i * 0.5 < GLIDE else 0.42)
pour(WATER - 0.1, 0.9, 0.3)
whoosh_in(tr, GLIDE + 0.4, 0.6, 0.35); pop(tr, GLIDE, 0.3)
# 12:00: Pops für Brot/Zwiebel/Bier, Bier einschenken, Literzähler
for t0 in (BREAD, ONION, BEER): pop(tr, t0, 0.35)
pour(LITER, 2.2, 0.3)
for i in range(4): clink(LITER + i / 2.2, 1500 + i * 200, 0.12, 0.5)
# Lohn: Stempel
stamp(WAGE + 0.5, 0.6); ding(tr, WAGE + 0.6, 0.2)
# 17:00: Arzt – Verband wird gewickelt
for i in range(6): tr.add(B[4] + 0.6 + i * 0.27, filt(noise(0.2), 800, 5000) * np.hanning(int(0.2 * SR)), 0.12, 0.35)
ding(tr, B[4] + 2.3, 0.2)
# Gräber / Nacht: Grillen (sichtbar Nacht), Öllampen
crickets(tr, TOMB + 1.0, B[5], 0.04)
drum(TOMB, 0.5, 0.6)
# Outro
for i in range(5): drum(B[5] + 0.1 + i * 0.2, 0.5, 0.9)
ding(tr, B[5] + 1.3)
for w in WIPES: whoosh_in(tr, w + 0.05, 0.45, 0.28)
facts = [(B[1], 0.8), (B[1], NOSLAVE - B[1] + 0.1), (B[1], TEAMS - B[1] + 0.1), (B[2], 1.0), (B[2], SLED - B[2] + 0.1), (B[3], 1.0), (B[3], LITER - B[3] + 0.1), (B[3], WAGE - B[3] + 0.1), (B[4], 0.9), (B[4], TOMB - B[4] + 0.1)]
for a, f in facts: pop(tr, a + f, 0.18)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
