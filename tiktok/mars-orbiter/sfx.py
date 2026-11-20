# Soundeffekte "Mars Climate Orbiter" – nur klar erkennbare Effekte; Bibliotheks-Geräusche haben Vorrang (snd)
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
T = dict(space=0, control=2.4, lisa=3.5, mars=4.55, journey=6.85, worry=8.85, screen=11.0, burn=13.15, behind=14.7, wait=16.75,
         nosignal=18.7, low=19.85, burnup=21.85, reason=23.55, units=24.2, nobody=27.35, money=29.6, end=32.85, out=38.5)
tr = Track(T['out'])


def beep(t0, f=1200, d=0.08, g=0.1, pan=0.5):
    tr.add(t0, np.sin(2 * np.pi * f * T_(d)) * np.hanning(int(d * SR)), g, pan)


def keys(t0, t1, g=0.1):
    k = t0
    while k < t1: tr.add(k, filt(noise(0.025), 2000, 8000) * np.exp(-T_(0.025) * 140), g, rng.uniform(0.3, 0.7)); k += rng.uniform(0.07, 0.14)


def flatline(t0, d, g=0.12):
    tr.add(t0, fade(np.sin(2 * np.pi * 1000 * T_(d)), 0.02, 0.2), g)


whoosh_in(tr, 1.2, 1.0, 0.15)
keys(T['control'] + 0.1, T['lisa'] + 0.4); for_ = [beep(T['control'] + 0.3 + i * 0.5, 1500, 0.06, 0.06) for i in range(2)]
pop(tr, T['lisa'] + 0.25, 0.15)
whoosh_in(tr, T['mars'] + 0.5, 0.8, 0.15)
for i in range(9): beep(T['journey'] + 0.2 + i * 0.2, 900 + i * 60, 0.06, 0.07)
heartbeat(tr, T['worry'], T['screen'], 80, 0.3)
beep(T['screen'] + 0.6, 700, 0.25, 0.1); beep(T['screen'] + 1.0, 700, 0.25, 0.1)   # Warnton
d = T['behind'] - T['burn']; tr.add(T['burn'], fade(filt(noise(d), 80, 1200), 0.1, 0.3), 0.3)   # Triebwerk
for i in range(6): beep(T['wait'] + 0.3 + i * 0.33, 1300, 0.05, 0.07)                          # Ticken / Warten
heartbeat(tr, T['behind'], T['nosignal'], 90, 0.35)
flatline(T['nosignal'] + 0.1, 1.0, 0.1); sub_drop(tr, T['nosignal'] + 0.05, 0.4, 1.2)
whoosh_in(tr, T['low'] + 0.6, 0.6, 0.15)
d = T['reason'] - T['burnup']; tr.add(T['burnup'], fade(filt(noise(d), 200, 3000), 0.1, 0.3), 0.25); crack(tr, T['burnup'] + 0.7, 0.3)
boom(tr, T['reason'] + 0.05, 0.3, 1.0)
pop(tr, T['units'] + 1.2, 0.2); pop(tr, T['units'] + 2.5, 0.2); ding(tr, T['units'] + 2.9, 0.22)
whoosh_in(tr, T['nobody'] + 0.5, 0.4, 0.1)
for i in range(12): tr.add(T['money'] + i * 0.1, filt(noise(0.06), 1500, 6000) * np.exp(-T_(0.06) * 50), 0.08, rng.uniform(0.3, 0.7))
ding(tr, T['money'] + 1.4, 0.2); ding(tr, T['end'] + 0.15, 0.2)
for k in [k for k in T if k not in ('space', 'out')]: whoosh_in(tr, T[k] + 0.03, 0.28, 0.08)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
