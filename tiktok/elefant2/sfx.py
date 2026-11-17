# Soundeffekte "Der Elefant – Teil 2" – ruhig, nur klar erkennbare Effekte
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
T = dict(circle=0, days=3.3, young=4.73, never=7.23, cross=9.45, nothing=11.5, watch=13.56, step=14.91, tug=16.16, snap=17.06, out=17.9,
         whole=18.74, sing=21.75, math=23.35, enough=24.85, yellow=26.8, end=29.89, fin=33.9)
tr = Track(T['fin'])


def creak(t0, d=0.5, g=0.14):
    tt = T_(d); f = 160 + 90 * np.sin(2 * np.pi * 1.7 * tt); s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (0.5 + 0.5 * np.sin(2 * np.pi * 27 * tt))
    tr.add(t0, fade(filt(s, 200, 2000), 0.05, 0.15), g, 0.35)


def thud(t0, g=0.3, pan=0.5):
    d = 0.3; tt = T_(d); tr.add(t0, np.sin(2 * np.pi * np.cumsum(110 * np.exp(-tt * 8) + 40) / SR) * np.exp(-tt * 14), g, pan)


def steps(t0, t1, rate, g=0.12, pan=0.5):
    k = t0
    while k < t1: thud(k, g, pan); k += 1 / rate


for k in np.arange(T['days'], T['young'], 0.18): tr.add(k, filt(noise(0.03), 1500, 6000) * np.exp(-T_(0.03) * 100), 0.06, 0.5)   # Licht flackert/Zeit
steps(T['young'] + 0.1, T['never'], 3, 0.08, 0.8); steps(T['cross'], T['watch'], 3, 0.08, 0.4)
ding(tr, T['nothing'] + 0.3, 0.12)
thud(T['step'] + 0.5, 0.35); creak(T['step'] + 0.3, 0.5, 0.15); creak(T['tug'], 0.8, 0.22)
crack(tr, T['snap'] + 0.05, 0.5, 0.4); boom(tr, T['snap'] + 0.05, 0.35, 1.2)
steps(T['out'], T['whole'], 2.5, 0.2, 0.3)
pop(tr, T['sing'] + 0.1, 0.15); pop(tr, T['math'] + 0.1, 0.15); ding(tr, T['math'] + 0.6, 0.15)
crack(tr, T['enough'] + 0.3, 0.25, 0.3); ding(tr, T['enough'] + 0.8, 0.18)
ding(tr, T['end'] + 1.6, 0.15)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
