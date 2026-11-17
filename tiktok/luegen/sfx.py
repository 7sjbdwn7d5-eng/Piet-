# Soundeffekte "Niemand kann lügen" – nur klar erkennbare Effekte zu sichtbaren Ereignissen
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
B = [0, 2.95, 10.8, 16.7, 22.9, 29.35, 37.0]
TRUTH = 1.55; ASK = B[1] + 1.85; HATE = B[1] + 3.95; AD = B[1] + 5.25; TV = B[2] + 3.0
CONF = B[3] + 1.9; GAVEL = B[3] + 2.5; SHOP = B[3] + 3.55; GIFT = B[4] + 3.3
tr = Track(B[-1])


def beep(t0, f=1200, d=0.08, g=0.12, pan=0.5):
    tr.add(t0, np.sin(2 * np.pi * f * T_(d)) * np.hanning(int(d * SR)), g, pan)


def knock(t0, g=0.5):
    d = 0.35; tt = T_(d); tr.add(t0, np.sin(2 * np.pi * np.cumsum(180 * np.exp(-tt * 10) + 70) / SR) * np.exp(-tt * 18) + 0.3 * filt(noise(d), 800, 4000) * np.exp(-tt * 60), g)


def blip(t0, f0=900, f1=1500, g=0.15):
    d = 0.12; tr.add(t0, chirp(f0, f1, d) * np.hanning(int(d * SR)), g)


# Hook: Lügendetektor – nervöses Kratzen, Alarmpiepen, dann ruhiger "Wahrheit"-Ton
d = TRUTH; tt = T_(d); tr.add(0.1, fade(filt(noise(d), 2000, 7000) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 6 * tt))), 0.05, 0.1), 0.08, 0.6)
for k in np.arange(0.2, TRUTH, 0.25): beep(k, 1500, 0.08, 0.1, 0.4)
ding(tr, TRUTH + 0.1, 0.25)
# Büro
blip(ASK); blip(HATE, 1500, 700, 0.18); boom(tr, HATE + 0.5, 0.25, 0.8)
whoosh_in(tr, AD + 0.05, 0.35, 0.25)
for i in range(2): tr.add(AD + 0.45 + i * 0.1, filt(noise(0.12), 2500, 8000) * np.hanning(int(0.12 * SR)), 0.12)   # Durchstreichen
knock(AD + 1.3, 0.4)                                                                                                  # Stempel
# Chat
for k in [B[2] + 0.3, B[2] + 1.5, B[2] + 1.85]: pop(tr, k, 0.18)
crack(tr, B[2] + 2.3, 0.35)
whoosh_in(tr, TV + 0.05, 0.35, 0.25)
for i in range(6): thud_t = TV + 0.35 + i * 0.13; tr.add(thud_t, np.sin(2 * np.pi * 120 * T_(0.08)) * np.exp(-T_(0.08) * 40), 0.15, 0.5 + i * 0.08)   # Schritte weg
knock(TV + 1.45, 0.35)
# Gericht
blip(B[3] + 0.9, 700, 1100, 0.12); blip(CONF, 1100, 600, 0.15)
knock(GAVEL, 0.7); knock(GAVEL + 0.12, 0.3)
whoosh_in(tr, SHOP + 0.05, 0.35, 0.25)
d = 0.9; tr.add(SHOP + 0.3, chirp(900, 300, d) * np.hanning(int(d * SR)), 0.1)   # Sterne fallen
pop(tr, SHOP + 1.2, 0.16); pop(tr, SHOP + 1.7, 0.16)
# Vertrauen
for i in range(6): pop(tr, B[4] + 1.0 + i * 0.27, 0.06 + 0.01 * i)
ding(tr, B[4] + 2.6, 0.2)
for i in range(4): bird(tr, B[4] + 0.3 + i * 0.6, 0.3 + 0.1 * i, 0.05)
whoosh_in(tr, GIFT + 0.05, 0.35, 0.25)
pop(tr, GIFT + 0.05, 0.22); blip(GIFT + 0.3); blip(GIFT + 1.3, 1500, 700, 0.18)
d = 0.8; tr.add(GIFT + 1.6, chirp(500, 250, d) * np.hanning(int(d * SR)), 0.12)   # trauriges "Wah-wah"
# Übergänge
for c in B[1:6]: whoosh_in(tr, c + 0.03, 0.3, 0.12)
ding(tr, B[5] + 1.7, 0.18)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
