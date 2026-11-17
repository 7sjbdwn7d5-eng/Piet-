# Soundeffekte "Der Zuschauer-Effekt" – ruhig, nur klar erkennbare Effekte zu sichtbaren Ereignissen
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
T = dict(exp=0, alone=1.55, smoke=5.41, report=7.16, again=10.73, strangers=12.03, calm=14.18, fill=16.58, one=18.08,
         dumb=20.13, collapse=21.68, crowd=23.98, think=25.93, trick=28.4, jacket=30.55, call=32.1, end=33.6, out=38.9)
tr = Track(T['out'])


def click(t0, g=0.3):
    d = 0.03; tt = T_(d); tr.add(t0, filt(noise(d), 2000, 9000) * np.exp(-tt * 300) + 0.3 * np.sin(2 * np.pi * 1800 * tt) * np.exp(-tt * 150), g)


def thud(t0, g=0.3, pan=0.5):
    d = 0.3; tt = T_(d); tr.add(t0, np.sin(2 * np.pi * np.cumsum(110 * np.exp(-tt * 8) + 40) / SR) * np.exp(-tt * 14), g, pan)


def pencil(t0, t1, g=0.08, pan=0.5):   # Stift kratzt auf Papier
    k = t0
    while k < t1:
        d = rng.uniform(0.08, 0.18); tr.add(k, filt(noise(d), 2500, 8000) * np.hanning(int(d * SR)), g, pan); k += d + rng.uniform(0.03, 0.12)


def hiss(t0, d, g=0.1):   # Rauch strömt aus dem Gitter
    tr.add(t0, fade(filt(noise(d), 1500, 6000), 0.4, 0.4), g, 0.25)


def cough(t0, g=0.25, pan=0.5):
    for o in (0, 0.22):
        d = 0.16; tt = T_(d); tr.add(t0 + o, filt(noise(d), 250, 2500) * np.exp(-tt * 18) * (1 + 0.5 * np.sin(2 * np.pi * 140 * tt)), g, pan)


def beep(t0, f=1400, g=0.12):
    tr.add(t0, np.sin(2 * np.pi * f * T_(0.09)) * np.hanning(int(0.09 * SR)), g, 0.7)


click(0.25); click(0.32, 0.15)                                  # Lampe
pencil(T['alone'] + 0.2, T['smoke'] + 1.2)
hiss(T['smoke'] + 0.1, T['report'] - T['smoke'] + 0.6, 0.1)
for i in range(5): thud(T['report'] + 0.5 + i * 0.42, 0.13, 0.5 + i * 0.08)   # Schritte zur Tür
click(T['report'] + 2.6, 0.25); thud(T['report'] + 2.7, 0.2, 0.8)             # Tür
ding(tr, T['report'] + 0.35, 0.16)
whoosh_in(tr, T['again'] + 0.3, 0.5, 0.15)
pencil(T['strangers'] + 0.4, T['fill'], 0.06, 0.35); pencil(T['strangers'] + 0.5, T['fill'], 0.06, 0.65)
hiss(T['calm'], T['dumb'] - T['calm'] - 0.2, 0.12)
cough(T['fill'] + 0.7, 0.22); cough(T['one'] + 0.4, 0.25); cough(T['one'] + 1.4, 0.2)
tr.add(T['one'] + 0.25, np.sin(2 * np.pi * 260 * T_(0.35)) * np.exp(-T_(0.35) * 6), 0.12)   # tiefer Ton bei 10 %
whoosh_in(tr, T['dumb'] + 0.05, 0.4, 0.2)
thud(T['collapse'] + 0.95, 0.45); boom(tr, T['collapse'] + 1.0, 0.25, 1.0)
for i in range(20): pop(tr, T['crowd'] + i / 12, 0.05 + 0.002 * i)
heartbeat(tr, T['crowd'], T['trick'], 70, 0.35)
pop(tr, T['think'] + 0.25, 0.18)
ding(tr, T['trick'] + 0.2, 0.18)
whoosh_in(tr, T['jacket'] + 0.2, 0.3, 0.15)
for i, f in enumerate([1336, 1336, 1477]): beep(T['call'] + 0.65 + i * 0.18, f)   # 1-1-2 wählen
ding(tr, T['end'] + 2.5, 0.15)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
