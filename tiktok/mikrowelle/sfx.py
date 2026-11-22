# Soundeffekte "Die Mikrowelle" – nur klar erkennbare Effekte; Bibliotheks-Geräusche haben Vorrang (snd)
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
T = dict(lab=0, spencer=1.8, radar=4.35, magnetron=6.8, pocket=8.65, choc=10.6, corn=12.85, popcorn=14.8,
         egg=16.75, lean=17.55, splat=18.9, patent=21.75, school=23.6, radarange=26.9, end=31.35, out=37.0)
tr = Track(T['out'])


def hum(t0, d, g=0.06):
    tt = T_(d); tr.add(t0, fade(np.sin(2 * np.pi * 120 * tt) + 0.5 * np.sin(2 * np.pi * 240 * tt), 0.2, 0.3), g)


def popk(t0, g=0.12):
    d = 0.05; tt = T_(d); tr.add(t0, filt(noise(d), 800, 5000) * np.exp(-tt * 80) + 0.5 * np.sin(2 * np.pi * 600 * tt) * np.exp(-tt * 60), g, rng.uniform(0.2, 0.8))


for i in range(3): tr.add(0.4 + i * 0.6, np.sin(2 * np.pi * 1500 * T_(0.06)) * np.hanning(int(0.06 * SR)), 0.05, 0.3)
pop(tr, T['lab'] + 0.5, 0.15); pop(tr, T['spencer'] + 0.3, 0.15)
for i in range(3): tr.add(T['radar'] + 0.3 + i * 0.6, np.sin(2 * np.pi * 1200 * T_(0.12)) * np.exp(-T_(0.12) * 20), 0.07)   # Radar-Ping
hum(T['magnetron'], T['corn'] - T['magnetron'] + 2.0 + (T['egg'] - T['corn']), 0.05)
tr.add(T['pocket'] + 0.2, fade(filt(noise(1.6), 300, 2500), 0.4, 0.5), 0.08)   # Brutzeln
tr.add(T['choc'] + 0.1, filt(noise(0.6), 200, 1200) * np.hanning(int(0.6 * SR)), 0.12)   # Schmatzen/Tropfen
boom(tr, T['choc'] + 0.05, 0.2, 0.8)
for i in range(4): tr.add(T['corn'] + 0.15 + i * 0.18, np.sin(2 * np.pi * 2200 * T_(0.04)) * np.exp(-T_(0.04) * 80), 0.07)   # Körner fallen
k = T['popcorn']
while k < T['egg'] - 0.1: popk(k, 0.14); k += rng.uniform(0.04, 0.12)
heartbeat(tr, T['lean'], T['splat'], 90, 0.3)
d = 0.25; tt = T_(d); tr.add(T['splat'], filt(noise(d), 200, 3000) * np.exp(-tt * 18), 0.45); boom(tr, T['splat'], 0.25, 0.6)
ding(tr, T['patent'] + 0.45, 0.2); tr.add(T['patent'] + 0.5, np.sin(2 * np.pi * np.cumsum(180 * np.exp(-T_(0.3) * 10) + 70) / SR) * np.exp(-T_(0.3) * 18), 0.4)
tr.add(T['school'] + 0.4, filt(noise(0.25), 1500, 7000) * np.hanning(int(0.25 * SR)), 0.1)
tr.add(T['radarange'] + 0.1, np.sin(2 * np.pi * np.cumsum(60 + 0 * T_(0.5)) / SR) * np.exp(-T_(0.5) * 6), 0.5); boom(tr, T['radarange'] + 0.1, 0.3, 1.0)
pop(tr, T['radarange'] + 2.2, 0.2)
tr.add(T['end'] + 0.2, (np.sin(2 * np.pi * 2093 * T_(0.6)) + np.sin(2 * np.pi * 2637 * T_(0.6))) * np.exp(-T_(0.6) * 6), 0.12)   # Mikrowellen-"Pling"
for k2 in [k2 for k2 in T if k2 not in ('lab', 'out', 'splat')]: whoosh_in(tr, T[k2] + 0.03, 0.28, 0.07)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
