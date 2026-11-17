# Soundeffekte "Ballonflucht – Teil 2" – nur klar erkennbare Effekte; echte Bibliotheks-Geräusche haben Vorrang (snd)
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
T = dict(search=0, clock=3.3, fam=4.66, sew2=6.5, weeks=9.35, date=10.8, night2=12.15, eight=13.25, burn=15.68, lift=16.7, high=18.0,
         cold=19.6, gas=20.64, land=23.55, where=25.15, police=26.18, ask=28.9, answer=30.0, ja=31.08, end=31.74, out=36.3)
tr = Track(T['out'])


def clink(t0, f, g=0.15, pan=0.5):
    tr.add(t0, (np.sin(2 * np.pi * f * T_(0.25)) + 0.5 * np.sin(2 * np.pi * f * 2.7 * T_(0.25))) * np.exp(-T_(0.25) * 18), g, pan)


def thud(t0, g=0.3, pan=0.5):
    d = 0.25; tt = T_(d); tr.add(t0, np.sin(2 * np.pi * np.cumsum(140 * np.exp(-tt * 8) + 50) / SR) * np.exp(-tt * 20), g, pan)


def typing(t0, t1, g=0.16):
    k = t0
    while k < t1: tr.add(k, filt(noise(0.03), 1500, 8000) * np.exp(-T_(0.03) * 120), g, 0.6); k += rng.uniform(0.08, 0.16)


def sewing(t0, t1, g=0.18):
    k = t0
    while k < t1: tr.add(k, filt(noise(0.02), 1500, 7000) * np.exp(-T_(0.02) * 150) + 0.4 * np.sin(2 * np.pi * 300 * T_(0.02)), g, 0.45); k += 1 / 15


def burner(t0, d, g=0.4):
    tt = T_(d); tr.add(t0, fade(filt(noise(d), 150, 2500) * (0.8 + 0.2 * np.sin(2 * np.pi * 13 * tt)), 0.05, 0.15), g)


def engine(t0, d, g=0.2):
    tt = T_(d); s = np.sin(2 * np.pi * np.cumsum(55 + 10 * np.sin(2 * np.pi * 0.5 * tt)) / SR) + 0.5 * filt(noise(d), 60, 300)
    tr.add(t0, fade(s, 0.4, 0.4), g, 0.7)


def cheer(t0, d, g=0.24):
    tt = T_(d); s = filt(noise(d), 500, 3500) * (0.6 + 0.4 * np.sin(2 * np.pi * 1.3 * tt) ** 2); tr.add(t0, fade(stereo(s, 0.03), 0.2, 0.5), g)


typing(0.4, T['clock'], 0.14); boom(tr, 0.1, 0.5, 1.5)
k = T['clock']
while k < T['fam']: clink(k, 2200, 0.18, 0.5); k += 0.5
sewing(T['sew2'], T['weeks'] - 0.05, 0.18)
for i in range(6): tr.add(T['weeks'] + i * 0.22, filt(noise(0.06), 1500, 6000) * np.exp(-T_(0.06) * 50), 0.16, 0.5)
boom(tr, T['date'] + 0.1, 0.5, 1.2)
crickets(tr, T['night2'], T['eight'], 0.04)
heartbeat(tr, T['eight'], T['burn'], 100, 0.5)
burner(T['burn'], 1.0, 0.5); burner(T['lift'] + 0.2, 0.8, 0.4); whoosh_in(tr, T['high'], 1.2, 0.3)
for i in range(6): tr.add(T['high'] + 0.1 + i * 0.22, np.sin(2 * np.pi * 1800 * T_(0.06)) * np.hanning(int(0.06 * SR)), 0.08, 0.7)   # Höhenmesser-Piepen
for i in range(4): tr.add(T['cold'] + 0.15 + i * 0.25, filt(noise(0.2), 400, 2500) * np.hanning(int(0.2 * SR)), 0.1, 0.5)  # Atem
for d0 in [0.1, 0.5, 1.0, 1.2, 1.7, 2.2]: burner(T['gas'] + d0, 0.18, 0.35)                                               # stotternder Brenner
thud(T['land'] + 0.7, 0.6); boom(tr, T['land'] + 0.75, 0.4, 1.0); crack(tr, T['land'] + 0.8, 0.3)
crickets(tr, T['where'], T['police'], 0.05)
engine(T['police'], 1.6, 0.25); thud(T['police'] + 1.3, 0.35, 0.7); thud(T['police'] + 1.5, 0.3, 0.7)   # Autotüren
heartbeat(tr, T['ask'], T['answer'] + 0.6, 120, 0.55)
cheer(T['ja'], T['end'] - T['ja'] + 1.5, 0.3); ding(tr, T['ja'] + 0.05, 0.3)
for _ in range(6): bird(tr, rng.uniform(T['end'] + 0.2, T['out'] - 1.0), rng.uniform(0.2, 0.8), 0.05)
ding(tr, T['end'] + 1.5, 0.22)
for k in [k for k in T if k not in ('search', 'out')]: whoosh_in(tr, T[k] + 0.03, 0.28, 0.1)
for a in [T['search'] + 1.2, T['sew2'] + 0.2, T['eight'] + 0.2, T['high'] + 0.2, T['land'] + 0.2, T['end'] + 0.6]: pop(tr, a, 0.15)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
