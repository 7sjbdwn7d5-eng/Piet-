# Soundeffekte "Ein Tag auf der ISS" – nur klar erkennbare Effekte; Bibliotheks-Geräusche haben Vorrang (snd)
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
T = dict(orbit=0, wake=3.0, bag=4.3, sunrise=6.34, again=8.15, loop=9.25, counter=12.15, pouch=14.49, salt=16.5,
         treadmill=20.41, bones=21.75, drink=25.24, urine=26.35, machine=28.9, end=31.66, out=37.6)
tr = Track(T['out'])


def hum(t0, d, g=0.04):
    tt = T_(d); tr.add(t0, fade(np.sin(2 * np.pi * 60 * tt) + 0.4 * np.sin(2 * np.pi * 120 * tt) + 0.3 * filt(noise(d), 200, 800), 0.4, 0.4), g)


def beep(t0, f=1200, d=0.08, g=0.06):
    tr.add(t0, np.sin(2 * np.pi * f * T_(d)) * np.hanning(int(d * SR)), g)


hum(T['wake'], T['end'] - T['wake'], 0.04)
for i in range(3): beep(T['wake'] + 0.2 + i * 0.25, 1400, 0.1, 0.07)   # Wecker
tr.add(T['bag'] + 0.3, filt(noise(0.5), 600, 3000) * np.hanning(int(0.5 * SR)), 0.08)   # Reißverschluss
whoosh_in(tr, T['sunrise'] + 1.2, 1.2, 0.15); ding(tr, T['sunrise'] + 1.4, 0.12)
pop(tr, T['again'] + 0.15, 0.15)
for i in range(16): pop(tr, T['counter'] + i * 0.12, 0.05 + 0.003 * i)
tr.add(T['pouch'] + 0.3, filt(noise(0.3), 1500, 7000) * np.hanning(int(0.3 * SR)), 0.1)   # Tüte knistert
for i in range(3): tr.add(T['salt'] + 0.3 + i * 0.25, filt(noise(0.06), 400, 3000) * np.exp(-T_(0.06) * 40), 0.12)   # Quetschen
k = T['treadmill'] + 0.2
while k < T['bones']: tr.add(k, np.sin(2 * np.pi * np.cumsum(140 * np.exp(-T_(0.15) * 8) + 50) / SR) * np.exp(-T_(0.15) * 25), 0.12); k += 0.3
sub_drop(tr, T['bones'] + 0.3, 0.3, 1.0)
tr.add(T['drink'] + 0.5, filt(noise(0.4), 300, 2000) * np.hanning(int(0.4 * SR)), 0.1)   # Schlürfen
pop(tr, T['urine'] + 0.4, 0.15); pop(tr, T['urine'] + 1.5, 0.15)
d = T['end'] - T['machine']; tr.add(T['machine'], fade(filt(noise(d), 200, 1500) * 0.7 + 0.3 * np.sin(2 * np.pi * 180 * T_(d)), 0.3, 0.4), 0.08)
ding(tr, T['machine'] + 1.6, 0.18); ding(tr, T['end'] + 0.2, 0.15)
for k2 in [k2 for k2 in T if k2 not in ('orbit', 'out')]: whoosh_in(tr, T[k2] + 0.03, 0.28, 0.07)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
