# Soundeffekte "Yamaguchi" – ruhig und respektvoll, nur klar erkennbare Effekte
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
T = dict(city=0, yama=2.15, shipyard=4.3, clock=6.8, flash=7.95, cloud=9.1, hurt=12.3, train=13.9, nagasaki=16.2,
         date=17.8, office=18.95, boss=21.7, clock2=23.3, flash2=25.0, cloud2=26.3, shock=27.85, survive=30.15, end=31.45, out=37.0)
tr = Track(T['out'])


def tick(t0, t1, g=0.12):
    k = t0
    while k < t1: tr.add(k, filt(noise(0.02), 2000, 8000) * np.exp(-T_(0.02) * 150), g, 0.5); k += 0.5


def chug(t0, t1, g=0.16):
    k = t0; i = 0
    while k < t1: tr.add(k, filt(noise(0.14), 200, 2500) * np.hanning(int(0.14 * SR)), g * (1 if i % 2 == 0 else 0.6), 0.5); k += 0.17; i += 1


for _ in range(4): bird(tr, rng.uniform(0.3, T['clock'] - 0.5), rng.uniform(0.2, 0.8), 0.05)
for i in range(6): tr.add(T['shipyard'] + 0.3 + i * 0.4, np.sin(2 * np.pi * 900 * T_(0.05)) * np.exp(-T_(0.05) * 60), 0.06, 0.7)   # Hammer in der Werft
tick(T['clock'] + 0.1, T['flash'])
tr.add(T['flash'] - 0.05, fade(filt(noise(0.5), 3000, 12000), 0.01, 0.4), 0.2)   # heller Zisch beim Blitz
boom(tr, T['cloud'] + 0.4, 0.7, 2.5); sub_drop(tr, T['cloud'] + 0.4, 0.5, 1.6)
heartbeat(tr, T['hurt'], T['train'], 60, 0.3)
chug(T['train'], T['nagasaki']); tr.add(T['train'] + 0.3, (np.sin(2 * np.pi * 620 * T_(0.7)) + 0.6 * np.sin(2 * np.pi * 780 * T_(0.7))) * np.hanning(int(0.7 * SR)), 0.08)
for _ in range(3): bird(tr, rng.uniform(T['nagasaki'], T['date'] - 0.3), 0.6, 0.05)
for i in range(4): tr.add(T['date'] + i * 0.07, filt(noise(0.2), 1500, 7000) * np.hanning(int(0.2 * SR)), 0.08)
pop(tr, T['boss'] + 0.25, 0.15)
tick(T['clock2'] + 0.1, T['flash2'])
tr.add(T['flash2'] - 0.05, fade(filt(noise(0.5), 3000, 12000), 0.01, 0.4), 0.2)
boom(tr, T['cloud2'] + 0.2, 0.65, 2.5); sub_drop(tr, T['cloud2'] + 0.2, 0.45, 1.6)
heartbeat(tr, T['shock'], T['end'], 70, 0.3)
ding(tr, T['end'] + 0.2, 0.15)
for k in [k for k in T if k not in ('city', 'out', 'flash', 'flash2', 'cloud', 'cloud2')]: whoosh_in(tr, T[k] + 0.03, 0.28, 0.06)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
