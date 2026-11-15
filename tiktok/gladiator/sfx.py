# Soundeffekte "Ein Tag als Gladiator" (spannende Fassung) – nur klar erkennbare Effekte
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
B = [0, 4.05, 9.0, 16.5, 23.4, 34.45, 39.8]
GATE, TRAIN, GERSTEN, ASH, GATEOPEN, ARENA, FOE = 2.3, 6.4, 12.85, 13.7, 17.6, 19.0, 21.1
FALL, THUMB, ALIVE, COINS, STAR = 24.9, 25.5, 27.3, 29.8, 31.25
WIPES = [TRAIN, ASH, ARENA, THUMB, COINS, STAR]
tr = Track(B[-1])

def drum(t0, g=0.6, low=1.0):
    d = 0.7; tt = T(d); f = 45 + 70 * np.exp(-tt * 18)
    s = np.sin(2 * np.pi * np.cumsum(f * low) / SR) * np.exp(-tt * 5) + filt(noise(d), 100, 900) * np.exp(-tt * 30) * 0.5
    tr.add(t0, s, g)
def drums(t0, t1, step, g=0.4, accent=4):
    k, i = t0, 0
    while k < t1: drum(k, g * (1.3 if i % accent == 0 else 0.8)); k += step; i += 1
def brass(f, d):
    tt = T(d); s = sum(np.sin(2 * np.pi * f * k * tt) / k ** 1.1 for k in range(1, 9))
    env = np.clip(tt / 0.04, 0, 1) * np.clip((d - tt) / 0.12, 0, 1) * (0.85 + 0.15 * np.sin(2 * np.pi * 5 * tt))
    return filt(s * env, hi=3500)
def fanfare(t0, g=0.22, notes=((0, 392, 0.22), (0.24, 523, 0.22), (0.48, 659, 0.22), (0.72, 784, 0.7))):
    for dt, f, d in notes: tr.add(t0 + dt, reverb(brass(f, d), 1.2, 0.3), g)
def clang(t0, g=0.4, pan=0.5):
    d = 0.9; tt = T(d)
    s = sum(a * np.sin(2 * np.pi * f * tt) * np.exp(-tt * k) for f, a, k in [(523, 1, 4), (1340, 0.7, 6), (2250, 0.5, 8), (3720, 0.35, 11)])
    s = s + np.pad(filt(noise(0.03), 2000, 9000) * np.exp(-T(0.03) * 90), (0, len(tt) - int(0.03 * SR))) * 1.5
    tr.add(t0, s, g, pan)
def thwack(t0, g=0.5):
    d = 0.18; tt = T(d); tr.add(t0, filt(noise(d), 300, 2500) * np.exp(-tt * 40) + np.sin(2 * np.pi * 180 * tt) * np.exp(-tt * 30), g, 0.6)
def whip(t0, g=0.35):
    d = 0.25; tt = T(d); tr.add(t0, filt(noise(d), 1500, 9000) * (tt / d) ** 4 * 3 + np.pad(filt(noise(0.02), 3000, 12000) * 2, (0, len(tt) - int(0.02 * SR))) * (tt > 0.2), g, 0.75)
def cheer(t0, d, g=0.25):
    tt = T(d); s = filt(noise(d), 400, 3500) * (0.6 + 0.4 * np.sin(2 * np.pi * 1.3 * tt) ** 2)
    for _ in range(12):
        a = rng.uniform(0, max(0.1, d - 0.4)); f0 = rng.uniform(350, 650); L = int(0.35 * SR); i = int(a * SR); seg = s[i:i + L]
        seg += 0.25 * chirp(f0, f0 * 1.3, 0.35)[:len(seg)] * np.hanning(L)[:len(seg)]
    tr.add(t0, fade(stereo(s, 0.03), 0.25, 0.6), g)
def clink(t0, f, g=0.15, pan=0.5):
    tr.add(t0, (np.sin(2 * np.pi * f * T(0.25)) + 0.5 * np.sin(2 * np.pi * f * 2.7 * T(0.25))) * np.exp(-T(0.25) * 18), g, pan)

# --- Hook: zwei Trommelschläge auf den Titel, Schwerthieb, Fanfare, Herz-Boom beim Tor
drum(0.05, 0.9, 0.8); drum(0.25, 0.9, 0.8)
tr.add(0.45, filt(noise(0.25), 2500, 12000) * (T(0.25) / 0.25) ** 2 * 1.5, 0.45); clang(0.62, 0.35)
fanfare(1.0, 0.22)
drums(1.6, B[1] - 0.2, 0.5, 0.3)
sub_drop(tr, GATE, 0.55, 1.4)
whoosh_in(tr, B[1], 0.9, 0.3)
# --- 06:00: Kette, Training mit Peitschenknall des Ausbilders
for i, dt in enumerate([0.35, 0.5, 0.62, 0.9]): clink(B[1] + dt, 1900 + i * 230, 0.12, 0.2)
n = 0
while TRAIN + (n + 0.55) / 2.6 < B[2]: thwack(TRAIN + (n + 0.55) / 2.6, 0.55); n += 1
whip(TRAIN + 1.2); drums(TRAIN, B[2], 0.77, 0.25)
# --- 12:00: Löffel, Stempel, Asche
for dt in [0.9, 1.7, 2.5]: clink(B[2] + dt, 1200, 0.1, 0.65)
drum(GERSTEN, 0.9, 0.7); pop(tr, GERSTEN, 0.3)
d = 1.5; tr.add(ASH + 0.3, fade(filt(noise(d), 3000, 10000) * (0.7 + 0.3 * np.sin(2 * np.pi * 9 * T(d))), 0.1, 0.3), 0.18, 0.6)
pop(tr, ASH + 1.0, 0.3)
drums(ASH, B[3] - 0.3, 0.6, 0.25)
# --- 15:00: Tunnel: nur Herzschlag, dann Torkette + Licht; Arena: Trommeln + Fanfare + Jubel
heartbeat(tr, B[3], ARENA, 100, 0.6)
for i in range(14): clink(GATEOPEN + i * 0.06, 800 + (i % 3) * 140, 0.1, 0.5)
whoosh_in(tr, GATEOPEN + 0.9, 1.0, 0.35)
fanfare(ARENA + 0.05, 0.22); cheer(ARENA, FOE - ARENA + 0.1, 0.3); drums(ARENA, FOE, 0.5, 0.45)
# Gegner: Stille-Schlag, Dreizack-Stoß
drum(FOE, 1.0, 0.6); heartbeat(tr, FOE + 0.2, B[4], 110, 0.5)
tr.add(FOE + 1.0, filt(noise(0.4), 600, 5000) * (T(0.4) / 0.4) ** 2 * 2, 0.4); clang(FOE + 1.3, 0.3)
# --- Kampf: schnelle Trommeln + Klingen
drums(B[4], FALL, 0.25, 0.4, 2)
n = 0
while B[4] + (n + 0.45) / 4 < FALL - 0.1: clang(B[4] + (n + 0.45) / 4, 0.42, 0.4 + 0.2 * (n % 2)); n += 1
# Sturz in Zeitlupe: tiefer Whoosh, dumpfer Aufprall, dann Stille + Herzschlag
d = 0.9; tr.add(FALL - 0.05, chirp(300, 60, d) * np.exp(-T(d) * 2) * 0.6 + filt(noise(d), 200, 1500) * np.hanning(int(d * SR)) * 0.6, 0.6)
drum(FALL + 0.5, 1.0, 0.5); clink(FALL + 0.75, 2400, 0.2, 0.2)
heartbeat(tr, FALL + 0.6, ALIVE, 120, 0.7)
# Daumen: Trommelwirbel schwillt an … Einschlag
k = THUMB + 0.4
while k < ALIVE - 0.05: tr.add(k, filt(noise(0.05), 150, 1200) * np.exp(-T(0.05) * 50), 0.3 * (0.3 + 0.7 * (k - THUMB) / (ALIVE - THUMB)), 0.5); k += 0.05
boom(tr, ALIVE, 0.8, 1.5); drum(ALIVE, 1.0, 0.8)
# Überlebt: Jubel + Fanfare
cheer(ALIVE + 0.2, 2.2, 0.3); fanfare(ALIVE + 0.3, 0.2)
# Münzen
for i in range(40): clink(COINS + rng.uniform(0.05, 1.4), rng.uniform(2600, 3600), 0.08, rng.uniform(0.2, 0.8))
# Star: Trommeln + Jubel + Fanfare
drums(STAR, B[5], 0.5, 0.4); cheer(STAR, B[5] - STAR + 0.3, 0.32); fanfare(STAR + 0.1, 0.2, ((0, 523, 0.2), (0.22, 659, 0.2), (0.44, 784, 0.2), (0.66, 1046, 0.8)))
# Outro: Trommelschlag pro Zeile, Schwerthieb, Ding
for i in range(4): drum(B[5] + 0.1 + i * 0.25, 0.7, 0.8)
tr.add(B[5] + 1.05, filt(noise(0.2), 2500, 12000) * (T(0.2) / 0.2) ** 2 * 1.5, 0.4); clang(B[5] + 1.2, 0.3)
ding(tr, B[5] + 1.4)
# Wisch-Übergänge + Pops
for w in WIPES: whoosh_in(tr, w + 0.05, 0.45, 0.28)
facts = [(B[1], 0.8), (B[1], TRAIN - B[1] + 0.1), (B[2], 1.0), (B[2], ASH - B[2] + 0.1), (B[3], GATEOPEN - B[3]), (B[3], ARENA - B[3] + 0.1), (B[3], FOE - B[3] + 0.1),
         (B[4], 1.2), (B[4], THUMB - B[4] + 0.1), (B[4], ALIVE - B[4] + 0.05), (B[4], COINS - B[4] + 0.1), (B[4], STAR - B[4] + 0.1)]
for a, f in facts: pop(tr, a + f, 0.2)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
