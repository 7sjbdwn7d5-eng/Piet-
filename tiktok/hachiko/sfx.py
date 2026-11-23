# Soundeffekte "Hachikō" – ruhig, nur klar erkennbare Effekte; Bibliotheks-Geräusche haben Vorrang (snd)
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
T = dict(tokyo=0, station=2.4, dog=4.4, name=6.6, ueno=7.75, train=9.75, hat=13.05, wait=14.7, kenji=16.6, watch=18.0,
         rain=19.75, years=21.3, paper=23.1, crowd=24.7, mystery=27.3, end=30.6, out=36.5)
tr = Track(T['out'])


def thud(t0, g=0.2, pan=0.5):
    d = 0.2; tt = T_(d); tr.add(t0, np.sin(2 * np.pi * np.cumsum(140 * np.exp(-tt * 8) + 50) / SR) * np.exp(-tt * 22), g, pan)


def bark(t0, g=0.25):   # kurzes, freundliches "Wuff"
    d = 0.18; tt = T_(d); f = 420 * np.exp(-tt * 3); tr.add(t0, (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * filt(noise(d), 300, 2000)) * np.exp(-tt * 12) * np.hanning(int(d * SR)) ** 0.3, g)


def chime(t0, g=0.12):   # Bahnhofsglocke
    for i, f in enumerate([880, 1100, 1320]): tr.add(t0 + i * 0.25, np.sin(2 * np.pi * f * T_(0.8)) * np.exp(-T_(0.8) * 5), g)


k = 0.3
while k < T['station']: thud(k, 0.08, 0.4 + (k % 1) * 0.2); k += 0.45   # Schritte
chime(T['station'] + 0.2)
bark(T['name'] + 0.3); bark(T['name'] + 0.6, 0.18)
for i in range(3): pop(tr, T['ueno'] + 0.5 + i * 0.4, 0.08)
d = T['hat'] - T['train']; tt = T_(d); tr.add(T['train'], fade(filt(noise(d), 100, 1500) * (0.6 + 0.4 * np.sin(2 * np.pi * 3 * tt) ** 2), 0.4, 0.6), 0.2)   # Zug fährt ein
tr.add(T['train'] + 0.8, filt(noise(0.6), 2000, 7000) * np.hanning(int(0.6 * SR)), 0.1)   # Bremsen-Zischen
sub_drop(tr, T['hat'], 0.3, 1.2)
heartbeat(tr, T['wait'], T['kenji'], 60, 0.25)
d = (T['years'] - T['rain']) / 2; tr.add(T['rain'], fade(filt(noise(d), 1500, 8000), 0.1, 0.2), 0.14)   # Regen
for i in range(10): tr.add(T['years'] + i * 0.16, filt(noise(0.12), 1500, 7000) * np.hanning(int(0.12 * SR)), 0.08, 0.3 + 0.04 * i)   # Kalenderblätter
tr.add(T['paper'] + 0.05, filt(noise(0.35), 1500, 7000) * np.hanning(int(0.35 * SR)), 0.16); ding(tr, T['paper'] + 0.6, 0.15)
for i in range(4): pop(tr, T['crowd'] + 0.4 + i * 0.5, 0.08)
bark(T['crowd'] + 1.2, 0.18)
tr.add(T['mystery'] + 0.1, filt(noise(0.5), 400, 3000) * np.hanning(int(0.5 * SR)), 0.1)   # Stoff raschelt
pop(tr, T['mystery'] + 0.6, 0.18); ding(tr, T['end'] + 0.2, 0.15)
for k2 in [k2 for k2 in T if k2 not in ('tokyo', 'out')]: whoosh_in(tr, T[k2] + 0.03, 0.28, 0.06)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
