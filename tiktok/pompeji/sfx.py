# Soundeffekte "Pompeji – Marcus und Felix" – nur klar erkennbare Effekte
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
from sfxlib import *
from sfxlib import T as T_
T = dict(dawn=0, bakery=3.9, dog=5.9, growl=7.85, quake=9.45, shrug=10.85, bang=12.8, plume=14.45, scale=16.7,
         pumice=18.55, roof=20.1, run=21.45, chain=23.05, flow=25.0, flee=27.85, end=29.6, cta=30.8, out=33.6)
tr = Track(T['out'])


def clink(t0, f, g=0.15, pan=0.5):
    tr.add(t0, (np.sin(2 * np.pi * f * T_(0.25)) + 0.5 * np.sin(2 * np.pi * f * 2.7 * T_(0.25))) * np.exp(-T_(0.25) * 18), g, pan)


def growl(t0, d=1.4, g=0.5):
    tt = T_(d); f = 95 + 25 * np.sin(2 * np.pi * 3 * tt)
    s = (np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.4 + filt(noise(d), 120, 900) * 1.2) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * tt) ** 2)
    tr.add(t0, fade(filt(s, 80, 1400), 0.15, 0.3), g, 0.45)


def whimper(t0, g=0.18):
    d = 0.6; tt = T_(d)
    s = np.sin(2 * np.pi * np.cumsum(900 + 500 * np.sin(np.pi * tt / d)) / SR) * np.hanning(int(d * SR))
    tr.add(t0, s, g, 0.55)


def thud(t0, g=0.3, pan=0.5):
    d = 0.25; tt = T_(d)
    tr.add(t0, np.sin(2 * np.pi * np.cumsum(140 * np.exp(-tt * 8) + 50) / SR) * np.exp(-tt * 20) + filt(noise(d), 500, 3000) * np.exp(-tt * 40) * 0.5, g, pan)


def steps(t0, t1, rate, g=0.2):
    k = t0; i = 0
    while k < t1:
        thud(k, g, 0.4 + 0.2 * (i % 2)); k += 1 / rate; i += 1


# Morgen: Vögel
for _ in range(8): bird(tr, rng.uniform(0.4, T['dog'] - 0.3), rng.uniform(0.2, 0.8), 0.06)
# Bäckerei: Brot aus dem Ofen
whoosh_in(tr, T['bakery'] + 0.6, 0.5, 0.2); ding(tr, T['bakery'] + 0.9, 0.15)
# Hund frisst nicht: Fiepen
whimper(T['dog'] + 0.6); whimper(T['dog'] + 1.4, 0.14)
# Knurren
growl(T['growl'] + 0.1, T['quake'] - T['growl'] - 0.1, 0.55)
# Beben: Amphoren klappern + kurzer Stoß
for i in range(26): clink(T['quake'] + i * 0.05, 700 + (i * 137) % 600, 0.09, 0.3 + 0.4 * ((i * 7) % 10) / 10)
boom(tr, T['quake'], 0.35, 1.2)
# KNALL
boom(tr, T['bang'], 1.0, 3.0); sub_drop(tr, T['bang'], 0.8, 2.0)
tr.add(T['bang'], filt(noise(0.4), 300, 6000) * np.exp(-T_(0.4) * 8), 0.6)
# Wolke steigt: anschwellendes Grollen (sichtbar)
d = T['scale'] - T['plume']; tr.add(T['plume'], fade(filt(noise(d), 40, 400) * 2 * (T_(d) / d), 0.3, 0.4), 0.35)
# Skala: Ticks
for i in range(7): pop(tr, T['scale'] + 0.1 + i * 0.1, 0.12)
# Steinregen
for _ in range(70): thud(rng.uniform(T['pumice'], T['run']), rng.uniform(0.08, 0.22), rng.uniform(0.1, 0.9))
# Dach kracht
boom(tr, T['roof'] + 0.4, 0.7, 2.0); crack(tr, T['roof'] + 0.4, 0.5); crack(tr, T['roof'] + 0.55, 0.4, 0.7)
# Marcus rennt: Herzschlag + Schritte
heartbeat(tr, T['run'], T['flow'], 120, 0.55); steps(T['run'], T['chain'], 4.5, 0.18)
# Kette + Fiepen
for i in range(18): clink(T['chain'] + 0.1 + i * 0.105, 1500 + (i % 3) * 300, 0.12, 0.25)
whimper(T['chain'] + 0.5, 0.2); whimper(T['chain'] + 1.3, 0.18)
# Glutwolke: tiefes, rollendes Donnern (sichtbar)
d = T['end'] - T['flow']; tr.add(T['flow'], fade(stereo(filt(noise(d), 30, 300) * 2.5 * (0.5 + 0.5 * T_(d) / d), 0.05), 0.5, 0.05), 0.45)
# Flucht
heartbeat(tr, T['flee'], T['end'], 150, 0.6); steps(T['flee'], T['end'], 6, 0.2); whoosh_in(tr, T['end'], 1.0, 0.4)
# Ende: Schlag, dann Stille; Ding beim Kommentar-Aufruf
boom(tr, T['end'], 0.8, 2.5); ding(tr, T['cta'] + 0.5, 0.25)
# leise Schnitt-Whooshes, Pops für REAL-Schilder
for k in ['bakery', 'dog', 'growl', 'quake', 'shrug', 'plume', 'scale', 'pumice', 'roof', 'run', 'chain', 'flow', 'flee']: whoosh_in(tr, T[k] + 0.03, 0.3, 0.12)
for t0 in [T['bakery'] + 0.4, T['quake'] + 0.3, T['scale'] + 0.2, T['pumice'] + 0.3, T['flow'] + 0.3, T['end'] + 0.6]: pop(tr, t0, 0.18)
tr.save(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav')
