# Soundeffekte "Juliane Koepcke" – nur klar erkennbare Effekte; Bibliotheks-Geräusche haben Vorrang (snd)
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
T = dict(jungle=0, juliane=2.35, plane=4.5, storm=6.87, bolt=8.05, breakup=9.85, fall=11.91, canopy=14.6,
         wake=16.65, injuries=17.95, alone=20.75, father=22.84, water=25.35, wade=27.11, hungry=28.75, hut=30.25, end=32.9, out=39.8)
tr = Track(T['out'])


def engine(t0, d, g=0.12):
    tt = T_(d); tr.add(t0, fade(np.sin(2 * np.pi * 95 * tt) * 0.6 + filt(noise(d), 80, 600), 0.4, 0.4), g)


def splash(t0, g=0.12):
    d = 0.3; tr.add(t0, filt(noise(d), 600, 5000) * np.exp(-T_(d) * 12), g, rng.uniform(0.3, 0.7))


engine(0, T['storm'] + 1.2, 0.1)
for _ in range(3): bird(tr, rng.uniform(0.3, T['plane']), rng.uniform(0.2, 0.8), 0.04)
d = T['bolt'] - T['storm']; tr.add(T['storm'], fade(filt(noise(d), 300, 6000), 0.3, 0.2), 0.12)   # Regen am Fenster
crack(tr, T['bolt'] + 0.4, 0.5); boom(tr, T['bolt'] + 0.45, 0.6, 2.0)
crack(tr, T['breakup'] + 0.3, 0.4); boom(tr, T['breakup'] + 0.3, 0.4, 1.5)
wind(tr, T['fall'], T['wake'] - 0.3, 0.3, 300, 2500)
for i in range(6): tr.add(T['canopy'] + 1.0 + i * 0.07, filt(noise(0.15), 800, 5000) * np.exp(-T_(0.15) * 20), 0.25, rng.uniform(0.3, 0.7))   # Äste brechen
thud = lambda t0, g: tr.add(t0, np.sin(2 * np.pi * np.cumsum(110 * np.exp(-T_(0.3) * 8) + 40) / SR) * np.exp(-T_(0.3) * 14), g)
thud(T['canopy'] + 1.4, 0.4)
crickets(tr, T['wake'], T['father'], 0.05)
for _ in range(6): bird(tr, rng.uniform(T['wake'], T['father']), rng.uniform(0.2, 0.8), 0.05)
heartbeat(tr, T['wake'], T['injuries'] + 1, 60, 0.3)
for i, k in enumerate([0.0, 1.3, 2.1]): pop(tr, T['injuries'] + k + 0.05, 0.12)
pop(tr, T['father'] + 1.5, 0.15)
d = T['end'] - T['water']; tr.add(T['water'], fade(filt(noise(d), 400, 3000) * 0.8, 0.5, 0.8), 0.08)   # Bach
k = T['wade']
while k < T['hungry']: splash(k, 0.1); k += 0.55
for i in range(10): tr.add(T['wade'] + i * 0.15, np.sin(2 * np.pi * (700 + i * 40) * T_(0.04)) * np.hanning(int(0.04 * SR)), 0.04)
ding(tr, T['hut'] + 0.8, 0.2)
for _ in range(4): bird(tr, rng.uniform(T['hut'], T['end']), 0.6, 0.05)
ding(tr, T['end'] + 0.2, 0.15)
for k2 in [k2 for k2 in T if k2 not in ('jungle', 'out', 'bolt', 'breakup')]: whoosh_in(tr, T[k2] + 0.03, 0.28, 0.06)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
