# Soundeffekte "Ein Tag als Gladiator" – nur klar erkennbare Effekte (Regel aus ANLEITUNG.md)
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
B = [0, 4.1, 9.9, 18.1, 24.4, 34.3, 39.4]
GATE, TRAIN, GERSTEN, ASH, ARENA, FOE = 2.3, 7.15, 14.25, 15.1, 19.05, 21.95
THUMB, ALIVE, COINS, STAR = 25.8, 27.75, 30.3, 32.1
WIPES = [TRAIN, ASH, ARENA, FOE, THUMB, ALIVE, COINS, STAR]
tr = Track(B[-1])

def brass(f, d):
    tt = T(d); s = sum(np.sin(2 * np.pi * f * k * tt) / k ** 1.1 for k in range(1, 9))
    env = np.clip(tt / 0.04, 0, 1) * np.clip((d - tt) / 0.12, 0, 1) * (0.85 + 0.15 * np.sin(2 * np.pi * 5 * tt))
    return filt(s * env, hi=3500)
def fanfare(t0, g=0.22):
    for dt, f, d in [(0, 392, 0.22), (0.24, 523, 0.22), (0.48, 659, 0.22), (0.72, 784, 0.7)]:
        tr.add(t0 + dt, reverb(brass(f, d), 1.2, 0.3), g)
def clang(t0, g=0.4, pan=0.5):
    d = 0.9; tt = T(d)
    s = sum(a * np.sin(2 * np.pi * f * tt) * np.exp(-tt * k) for f, a, k in [(523, 1, 4), (1340, 0.7, 6), (2250, 0.5, 8), (3720, 0.35, 11)])
    s = s + np.pad(filt(noise(0.03), 2000, 9000) * np.exp(-T(0.03) * 90), (0, len(tt) - int(0.03 * SR))) * 1.5
    tr.add(t0, s, g, pan)
def thwack(t0, g=0.5):
    d = 0.18; tt = T(d)
    s = filt(noise(d), 300, 2500) * np.exp(-tt * 40) + np.sin(2 * np.pi * 180 * tt) * np.exp(-tt * 30)
    tr.add(t0, s, g, 0.6)
def cheer(t0, d, g=0.25):
    tt = T(d); s = filt(noise(d), 400, 3500) * (0.6 + 0.4 * np.sin(2 * np.pi * 1.3 * tt) ** 2)
    for _ in range(12):   # einzelne Rufe
        a = rng.uniform(0, d - 0.4); f0 = rng.uniform(350, 650); L = int(0.35 * SR); i = int(a * SR)
        s[i:i + L] += 0.25 * chirp(f0, f0 * 1.3, 0.35)[:len(s[i:i + L])] * np.hanning(L)[:len(s[i:i + L])]
    tr.add(t0, fade(stereo(s, 0.03), 0.25, 0.6), g)
def clink(t0, f, g=0.15, pan=0.5):
    tr.add(t0, (np.sin(2 * np.pi * f * T(0.25)) + 0.5 * np.sin(2 * np.pi * f * 2.7 * T(0.25))) * np.exp(-T(0.25) * 18), g, pan)

# Hook: Fanfare, Herzschlag-Boom beim Tor
fanfare(0.15, 0.24)
sub_drop(tr, GATE, 0.5, 1.2)
whoosh_in(tr, B[1], 0.9, 0.3)
# Zelle: Kettenklirren beim Aufsetzen
for i, dt in enumerate([0.35, 0.5, 0.62, 0.9]): clink(B[1] + dt, 1900 + i * 230, 0.12, 0.2)
# Training: Holzschwert trifft Pfahl
n = 0
while True:
    t_hit = TRAIN + (n + 0.55) / 2.6
    if t_hit >= B[2]: break
    thwack(t_hit, 0.55); n += 1
# Essen: Löffel klappert, Stempel
for dt in [0.9, 1.7, 2.5, 3.3]: clink(B[2] + dt, 1200, 0.1, 0.65)
boom(tr, GERSTEN, 0.6, 1.0); pop(tr, GERSTEN, 0.3)
# Asche rieselt, Knochen "plopp"
d = 1.5; tr.add(ASH + 0.3, fade(filt(noise(d), 3000, 10000) * (0.7 + 0.3 * np.sin(2 * np.pi * 9 * T(d))), 0.1, 0.3), 0.18, 0.6)
pop(tr, ASH + 1.0, 0.3)
# Tunnel: Herzschlag + Torkette
heartbeat(tr, B[3], ARENA, 95, 0.55)
for i in range(10): clink(B[3] + 0.05 + i * 0.07, 900 + (i % 3) * 150, 0.09, 0.5)
# Arena: Fanfare + Jubel
fanfare(ARENA + 0.05, 0.2); cheer(ARENA, FOE - ARENA + 0.2, 0.28)
# Gegner: Schlag + Netz-Whoosh
boom(tr, FOE, 0.55, 1.2); tr.add(FOE + 0.4, filt(noise(0.5), 500, 4000) * np.hanning(int(0.5 * SR)), 0.25, 0.7)
# Kampf: Metallklingen
n = 0
while True:
    tc = B[4] + (n + 0.45) / 3
    if tc >= THUMB - 0.3: break
    clang(tc, 0.42, 0.4 + 0.2 * (n % 2)); n += 1
boom(tr, B[4] + 1.0, 0.5, 1.0)
# Daumen: Trommelwirbel bis zur Entscheidung
k = THUMB + 0.1
while k < ALIVE - 0.1:
    tr.add(k, filt(noise(0.05), 150, 1200) * np.exp(-T(0.05) * 50), 0.25 * (0.5 + 0.5 * (k - THUMB) / (ALIVE - THUMB)), 0.5); k += 0.055
boom(tr, ALIVE, 0.5, 1.0)
# Überlebt: Jubel + Ding
cheer(ALIVE + 0.3, 1.8, 0.22); ding(tr, ALIVE + 0.5, 0.25)
# Münzen
for i in range(40): clink(COINS + rng.uniform(0.05, 1.7), rng.uniform(2600, 3600), 0.08, rng.uniform(0.2, 0.8))
# Star: Jubel + Fanfare
cheer(STAR, B[5] - STAR + 0.3, 0.3); fanfare(STAR + 0.1, 0.18)
# Wisch-Übergänge
for w in WIPES: whoosh_in(tr, w + 0.05, 0.45, 0.28)
# UI-Pops bei Fakt-Karten und Outro
facts = [(B[1], 0.8), (B[1], TRAIN - B[1] + 0.1), (B[2], 1.1), (B[2], ASH - B[2] + 0.1), (B[3], 1.95), (B[3], FOE - B[3] + 0.1),
         (B[4], THUMB - B[4] + 0.1), (B[4], ALIVE - B[4] + 0.05), (B[4], COINS - B[4] + 0.1), (B[4], STAR - B[4] + 0.1)]
for a, f in facts: pop(tr, a + f)
for x in (0.1, 0.32, 0.54, 0.76): pop(tr, B[5] + x, 0.2)
ding(tr, B[5] + 1.3)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
