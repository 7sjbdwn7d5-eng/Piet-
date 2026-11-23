# Soundeffekte Lernvideo 1848/49 – dezent: Wisch bei jedem Szenenwechsel, Pop bei Einblendungen, Stempel
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
L = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lines.json')))
S = {l[3]: l[0] for l in L}; END = float(sys.argv[2]) if len(sys.argv) > 2 else L[-1][0] + 11
tr = Track(END)


def knock(t0, g=0.4):
    d = 0.35; tt = T_(d); tr.add(t0, np.sin(2 * np.pi * np.cumsum(180 * np.exp(-tt * 10) + 70) / SR) * np.exp(-tt * 18) + 0.3 * filt(noise(d), 800, 4000) * np.exp(-tt * 60), g)


for k, t0 in S.items():
    if k != 'intro': whoosh_in(tr, t0 + 0.03, 0.3, 0.08)
stamps = [('fuersten', 1.6), ('berlin', 6.3), ('gegen', 5.9), ('nein', 0.1), ('ende', 7.9), ('danach', 1.9)]
for k, o in stamps: knock(S[k] + o + 0.1, 0.4)
pops = [('bund', 5.0), ('bund', 6.2), ('ziele', 1.3), ('ziele', 3.4), ('paris', 3.6), ('pauls', 2.2), ('pauls', 6.0), ('schwach', 3.2), ('klein', 0.6), ('klein', 2.4),
        ('verf', 3.3), ('verf', 4.6), ('verf', 5.8), ('wahl', 1.8), ('gott', 1.6), ('gott', 3.4), ('kern', 1.5), ('kern', 2.9), ('kern', 4.1), ('reich', 3.3), ('reich', 5.0),
        ('heute', 1.4), ('a1', 5.0), ('a1', 5.6), ('a1', 6.2), ('a1', 7.2), ('a2', 2.0), ('a2', 3.0), ('a2', 4.0), ('a3', 2.0), ('a3', 5.0), ('a3', 7.0), ('merk', 1.2), ('merk', 3.4), ('merk', 5.6)]
for k, o in pops: pop(tr, S[k] + o, 0.12)
for i in range(12): tr.add(S['bund'] + 1.5 + i * 0.16, np.sin(2 * np.pi * (900 + i * 40) * T_(0.04)) * np.hanning(int(0.04 * SR)), 0.05)
ding(tr, S['intro'] + 0.3, 0.15); ding(tr, S['a1'] + 0.15, 0.15); ding(tr, S['merk'] + 7.6, 0.2)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
