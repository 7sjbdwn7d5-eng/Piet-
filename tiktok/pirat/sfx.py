# Soundeffekte "Pirat 1719" – nur klar erkennbare Effekte; Bibliotheks-Geräusche haben Vorrang (snd)
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
T = dict(sea=0, tom=2.3, food=5.45, capt=6.9, flag=8.42, pirates=10.15, surrender=12.65, ask=15.0, sign=17.4,
         vote=19.63, unvote=21.85, share=23.75, weeks=25.7, sick=28.25, scurvy=29.75, end=30.84, out=37.4)
tr = Track(T['out'])


def waves(t0, t1, g=0.1):
    d = t1 - t0; tt = T_(d); tr.add(t0, fade(stereo(filt(noise(d), 150, 1500) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.25 * tt) ** 2), 0.03), 0.5, 0.5), g)


def creak(t0, d=0.6, g=0.1):
    tt = T_(d); f = 160 + 80 * np.sin(2 * np.pi * 1.2 * tt); s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (0.5 + 0.5 * np.sin(2 * np.pi * 25 * tt))
    tr.add(t0, fade(filt(s, 200, 2000), 0.05, 0.2), g, 0.4)


def cheer(t0, d, g=0.2):
    tt = T_(d); s = filt(noise(d), 500, 3500) * (0.6 + 0.4 * np.sin(2 * np.pi * 1.3 * tt) ** 2); tr.add(t0, fade(stereo(s, 0.03), 0.2, 0.5), g)


waves(0, T['flag'], 0.12); waves(T['pirates'], T['end'], 0.08)
for _ in range(3): tr.add(rng.uniform(0.3, 2.0), np.sin(2 * np.pi * np.cumsum(1800 - 600 * T_(0.25)) / SR) * np.hanning(int(0.25 * SR)), 0.04, 0.7)   # Möwe
creak(T['tom'] + 0.4); creak(T['weeks'] + 0.4)
boom(tr, T['capt'] + 0.2, 0.25, 0.6)
heartbeat(tr, T['flag'], T['pirates'], 100, 0.35)
cheer(T['pirates'], 1.6, 0.25); for_ = [tr.add(T['pirates'] + 0.3 + i * 0.4, (np.sin(2 * np.pi * 2200 * T_(0.2)) * np.exp(-T_(0.2) * 25)), 0.08, 0.3 + 0.2 * i) for i in range(3)]   # Säbelklirren
pop(tr, T['ask'] + 1.2, 0.15)
k = T['sign'] + 0.3
while k < T['sign'] + 1.5: tr.add(k, filt(noise(0.08), 2500, 8000) * np.hanning(int(0.08 * SR)), 0.08); k += 0.11   # Feder kratzt
for i in range(5): pop(tr, T['vote'] + 0.3 + i * 0.12, 0.1)
cheer(T['vote'] + 0.8, 1.2, 0.15)
whoosh_in(tr, T['unvote'] + 0.9, 0.4, 0.2)
for i in range(16): tr.add(T['share'] + i * 0.075, np.sin(2 * np.pi * rng.uniform(2500, 4000) * T_(0.1)) * np.exp(-T_(0.1) * 35), 0.07, rng.uniform(0.3, 0.7))   # Münzen
heartbeat(tr, T['sick'], T['end'], 55, 0.3)
tr.add(T['scurvy'] + 0.1, np.sin(2 * np.pi * np.cumsum(180 * np.exp(-T_(0.3) * 10) + 70) / SR) * np.exp(-T_(0.3) * 18), 0.4)
ding(tr, T['end'] + 0.2, 0.15)
for k2 in [k2 for k2 in T if k2 not in ('sea', 'out')]: whoosh_in(tr, T[k2] + 0.03, 0.28, 0.07)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
