# Soundeffekte "Köpenick – Teil 2" – nur klar erkennbare Effekte; Bibliotheks-Geräusche haben Vorrang (snd)
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
T = dict(news=0, gone=0.9, laugh=3.2, paul=5.15, think=6.6, nogold=8.75, pass_=9.7, job=10.95, expel=12.7, noamt=14.55,
         cal=16.95, arrest=17.85, verdict=18.75, pardon=21.45, star=23.05, photos=24.45, you=27.3, end=28.85, out=34.6)
tr = Track(T['out'])


def thud(t0, g=0.3, pan=0.5):
    d = 0.25; tt = T_(d); tr.add(t0, np.sin(2 * np.pi * np.cumsum(140 * np.exp(-tt * 8) + 50) / SR) * np.exp(-tt * 20), g, pan)


def knock(t0, g=0.5):
    d = 0.35; tt = T_(d); tr.add(t0, np.sin(2 * np.pi * np.cumsum(180 * np.exp(-tt * 10) + 70) / SR) * np.exp(-tt * 18) + 0.3 * filt(noise(d), 800, 4000) * np.exp(-tt * 60), g)


def paperflip(t0, g=0.14):
    tr.add(t0, filt(noise(0.3), 1500, 7000) * np.hanning(int(0.3 * SR)), g)


def laugh(t0, t1, g=0.12):   # klare "Ha-ha"-Stöße
    k = t0
    while k < t1:
        d = 0.12; tt = T_(d); f = rng.uniform(180, 320)
        tr.add(k, (filt(noise(d), 400, 2500) * 0.6 + 0.6 * np.sin(2 * np.pi * f * tt)) * np.hanning(int(d * SR)), g, rng.uniform(0.2, 0.8)); k += rng.uniform(0.14, 0.22)


def shutter(t0, g=0.15):
    for o in (0, 0.05): tr.add(t0 + o, filt(noise(0.03), 2000, 9000) * np.exp(-T_(0.03) * 120), g, rng.uniform(0.3, 0.7))


paperflip(0.05, 0.2); whoosh_in(tr, 0.45, 0.4, 0.2); ding(tr, 0.4, 0.15)
whoosh_in(tr, T['gone'] + 0.5, 0.6, 0.15)
laugh(T['laugh'] + 0.1, T['paul'] - 0.1)
pop(tr, T['think'] + 0.95, 0.15)
crack(tr, T['nogold'] + 0.15, 0.2)
ding(tr, T['pass_'] + 0.15, 0.22)
pop(tr, T['job'] + 0.4, 0.15)
paperflip(T['expel']); knock(T['expel'] + 0.35, 0.5)
pop(tr, T['noamt'] + 0.5, 0.15); crack(tr, T['noamt'] + 0.75, 0.15)
for i in range(10): paperflip(T['cal'] + i * 0.07, 0.07)
thud(T['arrest'] + 0.05, 0.45); thud(T['arrest'] + 0.4, 0.3, 0.4); thud(T['arrest'] + 0.5, 0.3, 0.6)
for i in range(3): tr.add(T['verdict'] + 0.1 + i * 0.12, filt(noise(0.2), 300, 3000) * np.exp(-T_(0.2) * 15) + 0.4 * np.sin(2 * np.pi * 220 * T_(0.2)) * np.exp(-T_(0.2) * 12), 0.25)   # Gitter
knock(T['verdict'] + 0.5, 0.6)
knock(T['pardon'] + 0.25, 0.4); ding(tr, T['pardon'] + 0.5, 0.2)
for k in np.arange(T['star'] + 0.1, T['photos'], 0.35): shutter(k)
laugh(T['star'] + 0.2, T['photos'] - 0.1, 0.06)
for i in range(5): paperflip(T['photos'] + i * 0.15, 0.08)
heartbeat(tr, T['you'], T['end'], 70, 0.3)
ding(tr, T['end'] + 0.15, 0.2)
for k in [k for k in T if k not in ('news', 'out')]: whoosh_in(tr, T[k] + 0.03, 0.28, 0.08)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
