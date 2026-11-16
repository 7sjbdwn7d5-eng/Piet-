# Soundeffekte "Ballonflucht – Teil 1" – nur klar erkennbare Effekte; echte Bibliotheks-Geräusche haben Vorrang (snd)
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
T = dict(watch=0, family=2.55, plan=5.05, sew=7.2, shop=8.45, susp=11.55, night=13.6, pile=15.05, launch=17.27, rise=20.0,
         cloud=21.35, forest=24.32, sneak=26.45, left=28.42, stasi=29.7, end=31.54, out=35.6)
tr = Track(T['out'])
def clink(t0, f, g=0.15, pan=0.5):
    tr.add(t0, (np.sin(2 * np.pi * f * T_(0.25)) + 0.5 * np.sin(2 * np.pi * f * 2.7 * T_(0.25))) * np.exp(-T_(0.25) * 18), g, pan)
def sewing(t0, t1, g=0.18):
    k = t0
    while k < t1: tr.add(k, filt(noise(0.02), 1500, 7000) * np.exp(-T_(0.02) * 150) + 0.4 * np.sin(2 * np.pi * 300 * T_(0.02)), g, 0.45); k += 1 / 15
def burner(t0, d, g=0.4):
    tt = T_(d); tr.add(t0, fade(filt(noise(d), 150, 2500) * (0.8 + 0.2 * np.sin(2 * np.pi * 13 * tt)), 0.05, 0.15), g)
def twig(t0, g=0.25, pan=0.5): tr.add(t0, np.pad(filt(noise(0.05), 1500, 8000) * np.exp(-T_(0.05) * 70), (0, 2000)), g, pan)
def thud(t0, g=0.3, pan=0.5):
    d = 0.25; tt = T_(d); tr.add(t0, np.sin(2 * np.pi * np.cumsum(140 * np.exp(-tt * 8) + 50) / SR) * np.exp(-tt * 20), g, pan)
def sting(t0, g=0.6): boom(tr, t0, g, 1.8); tr.add(t0, filt(noise(0.3), 200, 2000) * np.exp(-T_(0.3) * 10), 0.3)

snd(tr, 0.2, 'herzschlag', 0.4, fallback=lambda: heartbeat(tr, 0.2, T['family'], 70, 0.45))
for i in range(6): tr.add(T['plan'] + 0.1 + i * 0.25, filt(noise(0.18), 1500, 6000) * np.hanning(int(0.18 * SR)), 0.12, 0.5)   # Bleistift
sewing(T['sew'], T['shop'] - 0.05, 0.2)
ding(tr, T['shop'] + 0.1, 0.2); ding(tr, T['shop'] + 1.15, 0.15); ding(tr, T['shop'] + 2.2, 0.15)               # Ladenglocken
sting(T['susp'] + 0.3, 0.45)
sewing(T['night'], T['pile'], 0.12)
for i in range(10): pop(tr, T['pile'] + i * 0.18, 0.14)
burner(T['launch'] + 0.1, 0.45); burner(T['launch'] + 1.0, 0.45); burner(T['launch'] + 1.9, 0.5); burner(T['rise'] + 0.1, 0.9, 0.35)
for i in range(30): clink(rng.uniform(T['cloud'], T['forest']), rng.uniform(1800, 3200), 0.06, rng.uniform(0.2, 0.8))  # Tropfen
for i in range(8): twig(T['forest'] + 1.0 + i * 0.09, 0.35, rng.uniform(0.3, 0.7))
thud(T['forest'] + 1.6, 0.5)
heartbeat(tr, T['sneak'], T['left'], 120, 0.5)
for i in range(10): twig(T['sneak'] + 0.1 + i * 0.2, 0.15, 0.3 + 0.4 * (i % 2))
for _ in range(5): bird(tr, rng.uniform(T['left'] + 0.1, T['stasi'] - 0.3), rng.uniform(0.2, 0.8), 0.05)
for i in range(6): thud(T['stasi'] - 0.3 + i * 0.28, 0.2, 0.4 + 0.2 * (i % 2))
sting(T['stasi'] + 0.1, 0.7)
heartbeat(tr, T['end'], T['out'] - 0.5, 80, 0.45); ding(tr, T['end'] + 1.6, 0.22)
for k in ['family', 'plan', 'sew', 'shop', 'susp', 'night', 'pile', 'launch', 'rise', 'cloud', 'forest', 'sneak', 'left', 'stasi', 'end']: whoosh_in(tr, T[k] + 0.03, 0.3, 0.1)
for a in [T['family'] + 0.2, T['shop'] + 0.2, T['launch'] + 0.2, T['forest'] + 0.2, T['stasi'] + 0.2]: pop(tr, a, 0.16)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
