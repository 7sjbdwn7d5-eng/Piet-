# Soundeffekte "Der Elefant und das Seil" – ruhig, nur klar erkennbare Effekte
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
T = dict(lamp=0, rope=1.2, stake=2.6, pull=4.35, pull2=5.1, days=6.2, hold=7.35, giveup=9.12, learn=10.47, noway=11.57,
         years=13.11, tug=15.2, snap=16.1, never=17.26, dumb=19.64, child=21.2, sing=23.0, math=24.1, today=25.84, torn=27.7, end=30.42, out=34.4)
tr = Track(T['out'])


def click(t0, g=0.3):
    d = 0.03; tt = T_(d); tr.add(t0, filt(noise(d), 2000, 9000) * np.exp(-tt * 300) + 0.3 * np.sin(2 * np.pi * 1800 * tt) * np.exp(-tt * 150), g)


def creak(t0, d=0.5, g=0.14):
    tt = T_(d); f = 160 + 90 * np.sin(2 * np.pi * 1.7 * tt); s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (0.5 + 0.5 * np.sin(2 * np.pi * 27 * tt))
    tr.add(t0, fade(filt(s, 200, 2000), 0.05, 0.15), g, 0.35)


def thud(t0, g=0.3, pan=0.5):
    d = 0.3; tt = T_(d); tr.add(t0, np.sin(2 * np.pi * np.cumsum(110 * np.exp(-tt * 8) + 40) / SR) * np.exp(-tt * 14), g, pan)


click(0.25); click(0.32, 0.15)
for k in [T['pull'] + 0.1, T['pull'] + 0.55, T['pull2'] + 0.05, T['pull2'] + 0.35, T['pull2'] + 0.7, T['days'] + 0.2, T['days'] + 0.6, T['days'] + 1.0]: creak(k, 0.35, 0.16)
for k in np.arange(T['pull'], T['hold'], 0.45): thud(k, 0.12, 0.6)
thud(T['giveup'] + 0.7, 0.4)
pop(tr, T['learn'] + 0.1, 0.15)
for k in np.arange(T['years'], T['years'] + 1.6, 0.4): thud(k, 0.18 + (k - T['years']) * 0.1, 0.6)
whoosh_in(tr, T['snap'] + 0.45, 0.5, 0.18)
for k in np.arange(T['never'] + 0.2, T['never'] + 1.6, 0.4): thud(k, 0.1, 0.8)
whoosh_in(tr, T['dumb'] + 0.05, 0.4, 0.2)
pop(tr, T['sing'] + 0.2, 0.18); pop(tr, T['math'] + 0.2, 0.18)
tr.add(T['math'] + 0.15, filt(noise(0.25), 1500, 7000) * np.hanning(int(0.25 * SR)), 0.1, 0.35)   # Papier
crack(tr, T['torn'] + 0.2, 0.25, 0.3); ding(tr, T['torn'] + 1.2, 0.18)
heartbeat(tr, T['today'], T['torn'], 70, 0.3)
ding(tr, T['end'] + 1.7, 0.15)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
