# Soundeffekte "Der Hauptmann von Köpenick" – nur klar erkennbare Effekte; Bibliotheks-Geräusche haben Vorrang (snd)
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
T = dict(city=0, paul=2.05, coup=4.0, halt=6.75, order=8.65, obey=9.5, train=11.1, rathaus=12.85, mayor=14.85, cash=17.2, money=19.25,
         twist=20.8, voigt=22.75, shoe=24.2, troedel=24.95, nomoney=27.4, end=29.55, out=36.0)
tr = Track(T['out'])


def thud(t0, g=0.3, pan=0.5):
    d = 0.25; tt = T_(d); tr.add(t0, np.sin(2 * np.pi * np.cumsum(140 * np.exp(-tt * 8) + 50) / SR) * np.exp(-tt * 20), g, pan)


def hoof(t0, t1, g=0.12):
    k = t0
    while k < t1:
        for o in (0, 0.09): tr.add(k + o, filt(noise(0.04), 600, 3000) * np.exp(-T_(0.04) * 90), g, 0.3 + 0.4 * (k - t0) / (t1 - t0))
        k += 0.38


def march(t0, t1, g=0.2):
    k = t0
    while k < t1: thud(k, g, 0.5); tr.add(k, filt(noise(0.05), 1500, 6000) * np.exp(-T_(0.05) * 80), g * 0.5); k += 0.42


def chug(t0, t1, g=0.18):
    k = t0; i = 0
    while k < t1: tr.add(k, filt(noise(0.14), 200, 2500) * np.hanning(int(0.14 * SR)), g * (1 if i % 2 == 0 else 0.6), 0.5); k += 0.17; i += 1


def coins(t0, n, g=0.12):
    for i in range(n): f = rng.uniform(2500, 4200); d = 0.12; tr.add(t0 + i * rng.uniform(0.03, 0.08), np.sin(2 * np.pi * f * T_(d)) * np.exp(-T_(d) * 30), g, rng.uniform(0.3, 0.7))


hoof(0.2, T['paul'] - 0.1)
march(T['coup'], T['halt'] + 0.6)
thud(T['halt'] + 0.95, 0.4); thud(T['halt'] + 1.0, 0.3)          # Hacken zusammen
boom(tr, T['order'] + 0.02, 0.35, 1.0)
for i in range(4): tr.add(T['obey'] + 0.1 + i * 0.05, filt(noise(0.05), 1500, 6000) * np.exp(-T_(0.05) * 80), 0.15, 0.5)   # Salut
march(T['obey'] + 0.6, T['train'], 0.16)
chug(T['train'], T['rathaus'] - 0.1); tr.add(T['train'] + 0.2, (np.sin(2 * np.pi * 620 * T_(0.7)) + 0.6 * np.sin(2 * np.pi * 780 * T_(0.7))) * np.hanning(int(0.7 * SR)), 0.1)  # Pfiff
march(T['rathaus'] + 0.1, T['rathaus'] + 1.1, 0.16)
for i in range(3): tr.add(T['rathaus'] + 1.4 + i * 0.5, np.sin(2 * np.pi * 440 * T_(0.6)) * np.exp(-T_(0.6) * 4), 0.08)   # Turmuhr
heartbeat(tr, T['mayor'], T['cash'], 100, 0.35)
tr.add(T['cash'] + 0.05, filt(noise(0.4), 300, 2000) * np.hanning(int(0.4 * SR)), 0.15)   # Deckel knarrt
ding(tr, T['cash'] + 0.5, 0.15); coins(T['cash'] + 0.9, 8, 0.1)
coins(T['money'], 30, 0.09); ding(tr, T['money'] + 1.2, 0.22)
whoosh_in(tr, T['twist'] + 0.85, 0.35, 0.25); sub_drop(tr, T['twist'] + 0.9, 0.4, 1.0)
whoosh_in(tr, T['voigt'] + 0.3, 0.4, 0.25)
for i in range(5): thud(T['shoe'] + i * 0.15, 0.18, 0.6); tr.add(T['shoe'] + i * 0.15, filt(noise(0.03), 2000, 7000) * np.exp(-T_(0.03) * 100), 0.12)   # Hammer
tr.add(T['troedel'] + 0.1, (np.sin(2 * np.pi * 2600 * T_(0.5)) + np.sin(2 * np.pi * 3100 * T_(0.5))) * np.exp(-T_(0.5) * 7), 0.08)   # Ladenglocke
pop(tr, T['troedel'] + 0.35, 0.15)
for i in range(3): pop(tr, T['nomoney'] + 0.2 + i * 0.25, 0.12)
heartbeat(tr, T['nomoney'], T['end'], 70, 0.3)
ding(tr, T['end'] + 0.15, 0.2); ding(tr, T['end'] + 2.3, 0.15)
for k in [k for k in T if k not in ('city', 'out', 'shoe', 'money')]: whoosh_in(tr, T[k] + 0.03, 0.28, 0.08)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
