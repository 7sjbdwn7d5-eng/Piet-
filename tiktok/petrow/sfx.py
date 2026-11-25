# Soundeffekte "Stanislaw Petrow" – nur klar erkennbare Effekte; Bibliotheks-Geräusche haben Vorrang (snd)
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
T = dict(moscow=0, room=2.35, dima=4.45, petrow=6.15, alarm=7.64, map=9.0, five=13.08, phone=15.35, retaliate=17.4,
         stare=20.32, think=21.7, call=25.48, wait=27.05, relief=30.12, sun=31.0, end=34.63, out=39.6)
tr = Track(T['out'])


def hum(t0, d, g=0.05):
    tt = T_(d); tr.add(t0, fade(np.sin(2 * np.pi * 50 * tt) + 0.5 * np.sin(2 * np.pi * 100 * tt), 0.3, 0.3), g)


def siren(t0, d, g=0.12):
    tt = T_(d); f = 700 + 250 * np.sign(np.sin(2 * np.pi * 1.6 * tt)); tr.add(t0, fade(np.sin(2 * np.pi * np.cumsum(f) / SR), 0.05, 0.2), g)


def beep(t0, f=1200, d=0.08, g=0.08):
    tr.add(t0, np.sin(2 * np.pi * f * T_(d)) * np.hanning(int(d * SR)), g)


crickets(tr, 0.2, T['room'], 0.04)
hum(T['room'], T['alarm'] - T['room'], 0.05)
for i in range(4): beep(T['room'] + 0.4 + i * 0.9, 1500, 0.05, 0.05)
siren(T['alarm'], T['stare'] - T['alarm'] + 0.5, 0.1)
for i in range(5): beep(T['five'] + i * 0.45, 900 + i * 120, 0.12, 0.12)
tr.add(T['phone'] + 0.2, (np.sin(2 * np.pi * 440 * T_(0.8)) + np.sin(2 * np.pi * 480 * T_(0.8))) * (np.sin(2 * np.pi * 20 * T_(0.8)) > 0) * 0.5, 0.08)   # Telefonklingeln
tr.add(T['retaliate'] + 0.1, fade(filt(noise(1.6), 60, 600), 0.3, 0.5), 0.2); boom(tr, T['retaliate'] + 0.9, 0.3, 1.5)
heartbeat(tr, T['stare'], T['call'], 100, 0.4)
tr.add(T['call'] + 0.05, filt(noise(0.06), 1500, 6000) * np.exp(-T_(0.06) * 60), 0.2)   # Hörer abnehmen
k = T['wait']
while k < T['relief']: tr.add(k, filt(noise(0.03), 2000, 8000) * np.exp(-T_(0.03) * 150), 0.14); k += 0.5   # Uhr tickt
ding(tr, T['relief'] + 0.1, 0.2)
hum(T['sun'], T['end'] - T['sun'], 0.03); whoosh_in(tr, T['sun'] + 0.9, 0.5, 0.15)
ding(tr, T['end'] + 0.2, 0.15)
for k2 in [k2 for k2 in T if k2 not in ('moscow', 'out', 'alarm')]: whoosh_in(tr, T[k2] + 0.03, 0.28, 0.06)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
