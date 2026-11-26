# Soundeffekte "Pompeji Teil 2" – nur klar erkennbare Effekte; Bibliotheks-Geräusche haben Vorrang (snd)
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
T = dict(title=0, flow=0.9, run=3.2, pumice=6.32, crowd=8.85, harbor=11.34, dogpull=13.45, dark=16.72, hit=18.4,
         far=21.09, many=23.05, map=26.59, newlife=28.7, end=31.46, out=37.5)
tr = Track(T['out'])


def rumble(t0, d, g=0.3):
    tr.add(t0, fade(stereo(filt(noise(d), 30, 300) * 2.0, 0.04), 0.3, 0.5), g)


def steps(t0, t1, rate, g=0.12):
    k = t0
    while k < t1: tr.add(k, np.sin(2 * np.pi * np.cumsum(140 * np.exp(-T_(0.2) * 8) + 50) / SR) * np.exp(-T_(0.2) * 22), g, rng.uniform(0.4, 0.6)); k += 1 / rate


def pebbles(t0, t1, g=0.06):
    k = t0
    while k < t1: tr.add(k, filt(noise(0.03), 1500, 6000) * np.exp(-T_(0.03) * 120), g, rng.uniform(0.1, 0.9)); k += rng.uniform(0.03, 0.09)


def bark(t0, g=0.25):
    d = 0.18; tt = T_(d); f = 420 * np.exp(-tt * 3); tr.add(t0, (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * filt(noise(d), 300, 2000)) * np.exp(-tt * 12), g)


boom(tr, 0.05, 0.4, 1.5)
rumble(T['flow'], T['pumice'] - T['flow'], 0.35)
steps(T['run'], T['pumice'], 3.5, 0.14); heartbeat(tr, T['run'], T['pumice'], 120, 0.3)
pebbles(T['pumice'], T['harbor'])
steps(T['crowd'], T['harbor'], 5, 0.1)
d = T['dogpull'] - T['harbor']; tr.add(T['harbor'], fade(filt(noise(d), 100, 1200) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * T_(d))), 0.3, 0.3), 0.25)   # Brandung
bark(T['dogpull'] + 0.3); bark(T['dogpull'] + 0.6, 0.18); steps(T['dogpull'], T['dark'], 4, 0.12)
tr.add(T['dark'] + 0.2, fade(filt(noise(T['hit'] - T['dark']), 800, 4000) * 0.4, 0.2, 0.3), 0.06)   # Fackel knistert
rumble(T['hit'], T['far'] - T['hit'], 0.45); boom(tr, T['hit'] + 0.3, 0.5, 2.0)
for _ in range(3): bird(tr, rng.uniform(T['many'], T['map']), rng.uniform(0.2, 0.8), 0.05)
steps(T['many'], T['map'], 3, 0.06)
ding(tr, T['map'] + 1.4, 0.18)
for _ in range(4): bird(tr, rng.uniform(T['newlife'], T['end']), 0.5, 0.05)
bark(T['newlife'] + 0.8, 0.2)
ding(tr, T['end'] + 0.2, 0.15)
for k2 in [k2 for k2 in T if k2 not in ('title', 'out', 'hit')]: whoosh_in(tr, T[k2] + 0.03, 0.28, 0.07)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
