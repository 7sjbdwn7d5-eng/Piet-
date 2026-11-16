# Soundeffekte "Tunnel 57" – nur klar erkennbare Effekte; echte Bibliotheks-Geräusche haben Vorrang (snd)
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
T = dict(aerial=0, wall=2.61, bakery=4.91, cellar=7.61, depth=9.8, cm70=11.36, crawl=13.19, buckets=15.06, months=17.4, meters=18.59, east=20.52, exit=21.33, toilet=22.23, tokio=24.18, escape=26.1, free=28.3, digger=29.96, space=31.86, end=33.51, out=37.18)
tr = Track(T['out'])


def clink(t0, f, g=0.15, pan=0.5):
    tr.add(t0, (np.sin(2 * np.pi * f * T_(0.25)) + 0.5 * np.sin(2 * np.pi * f * 2.7 * T_(0.25))) * np.exp(-T_(0.25) * 18), g, pan)


def thud(t0, g=0.3, pan=0.5):
    d = 0.25; tt = T_(d); tr.add(t0, np.sin(2 * np.pi * np.cumsum(140 * np.exp(-tt * 8) + 50) / SR) * np.exp(-tt * 20), g, pan)


def steps(t0, t1, rate, g=0.18):
    k = t0; i = 0
    while k < t1: thud(k, g, 0.4 + 0.2 * (i % 2)); k += 1 / rate; i += 1


def dig(t0, g=0.3):   # Spaten: Kratzen + dumpfer Stich
    tr.add(t0, filt(noise(0.12), 600, 4000) * np.hanning(int(0.12 * SR)), g * 0.6, 0.5); thud(t0 + 0.1, g)


def scrape(t0, d, g=0.12):
    tt = T_(d); tr.add(t0, fade(filt(noise(d), 300, 2500) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 1.5 * tt))), 0.1, 0.2), g)


def creak(t0, d=0.7, g=0.18):
    tt = T_(d); f = 180 + 120 * np.sin(2 * np.pi * 1.3 * tt); s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (0.5 + 0.5 * np.sin(2 * np.pi * 23 * tt))
    tr.add(t0, fade(filt(s, 200, 2200), 0.05, 0.2), g, 0.6)


def boing(t0, g=0.3):
    d = 0.5; tt = T_(d); tr.add(t0, np.sin(2 * np.pi * np.cumsum(220 + 300 * np.exp(-tt * 6) * np.cos(2 * np.pi * 9 * tt)) / SR) * np.exp(-tt * 5), g)


def cheer(t0, d, g=0.22):
    tt = T_(d); s = filt(noise(d), 500, 3500) * (0.6 + 0.4 * np.sin(2 * np.pi * 1.3 * tt) ** 2); tr.add(t0, fade(stereo(s, 0.03), 0.2, 0.5), g)


whoosh_in(tr, 0.6, 0.6, 0.25)
steps(T['wall'] + 0.2, T['bakery'], 2.2, 0.14)
ding(tr, T['bakery'] + 0.4, 0.18); steps(T['bakery'] + 0.2, T['cellar'], 4, 0.16)
for i in range(6): dig(T['cellar'] + 0.1 + i * 0.35, 0.3)
whoosh_in(tr, T['depth'] + 0.9, 0.9, 0.2); pop(tr, T['depth'] + 1.2, 0.25)
pop(tr, T['cm70'] + 0.3, 0.25)
scrape(T['crawl'], T['buckets'] - T['crawl'], 0.14)
for i in range(4): clink(T['buckets'] + 0.2 + i * 0.4, 900 + i * 80, 0.12, 0.4)
scrape(T['buckets'], 1.7, 0.12)
for i in range(6): tr.add(T['months'] + 0.1 + i * 0.23, filt(noise(0.06), 1500, 6000) * np.exp(-T_(0.06) * 50), 0.14, 0.5)
for i in range(14): pop(tr, T['meters'] + 0.1 + i * 0.12, 0.08)
crack(tr, T['east'] + 0.4, 0.4); whoosh_in(tr, T['exit'], 0.6, 0.25)
creak(T['toilet'] - 0.05, 0.6, 0.22); boing(T['toilet'] + 0.55, 0.35)
ding(tr, T['tokio'] + 0.7, 0.18)
heartbeat(tr, T['escape'], T['free'], 110, 0.45); scrape(T['escape'], T['free'] - T['escape'], 0.12)
cheer(T['free'] + 0.2, 1.8, 0.24); ding(tr, T['free'] + 0.8, 0.2)
whoosh_in(tr, T['space'], 0.8, 0.3)
d = T['end'] - T['space']; tr.add(T['space'], fade(stereo(filt(noise(d), 40, 500) * 2.0, 0.04), 0.3, 0.6), 0.3)
ding(tr, T['end'] + 1.5, 0.22)
for k in ['wall', 'bakery', 'cellar', 'depth', 'cm70', 'crawl', 'buckets', 'months', 'meters', 'east', 'exit', 'toilet', 'tokio', 'escape', 'free', 'digger', 'space', 'end']:
    whoosh_in(tr, T[k] + 0.03, 0.28, 0.1)
for a in [T['bakery'] + 0.2, T['depth'] + 0.2, T['buckets'] + 0.2, T['toilet'] + 0.2, T['escape'] + 0.2, T['space'] + 0.2]: pop(tr, a, 0.15)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
