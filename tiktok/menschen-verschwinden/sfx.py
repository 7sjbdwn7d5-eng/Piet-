# Synthetisiert alle Soundeffekte (keine Samples nötig) als Stereo-WAV, passend zu den Video-Zeiten.
# Usage: python3 sfx.py sfx.wav
import numpy as np, wave, sys
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100
B = [0, 3.0, 10.0, 17.0, 23.6, 31.6, 36.5]          # Schnitte im Video (= VIDEO_BOUNDS)
SB = [0, 3.6, 12.2, 20.8, 29.8, 39.2, 44]           # dieselben Schnitte in Szenen-Zeit (= SCENE_BOUNDS)
DUR = B[-1]
n = int(SR * DUR)
out = np.zeros((n, 2))
rng = np.random.default_rng(42)

def v(ts):
    """Szenen-Zeit -> Video-Zeit"""
    for i in range(len(SB) - 1):
        if ts < SB[i + 1] or i == len(SB) - 2:
            return B[i] + (ts - SB[i]) / (SB[i + 1] - SB[i]) * (B[i + 1] - B[i])

def filt(x, lo=None, hi=None, order=4):
    if lo and hi: sos = butter(order, [lo, hi], 'bandpass', fs=SR, output='sos')
    elif lo: sos = butter(order, lo, 'highpass', fs=SR, output='sos')
    else: sos = butter(order, hi, 'lowpass', fs=SR, output='sos')
    return sosfilt(sos, x)

def add(t0, sig, gain=1.0, pan=0.5):
    i0 = int(t0 * SR)
    if i0 >= n: return
    if sig.ndim == 1:
        sig = np.stack([sig * np.sqrt(1 - pan), sig * np.sqrt(pan)], 1)
    m = min(len(sig), n - max(i0, 0))
    out[max(i0, 0):max(i0, 0) + m] += sig[:m] * gain

def T(d): return np.arange(int(d * SR)) / SR
def fade(sig, fi=0.05, fo=0.05):
    L = len(sig); e = np.ones(L)
    a, b = int(fi * SR), int(fo * SR)
    if a: e[:a] = np.linspace(0, 1, a)
    if b: e[-b:] = np.minimum(e[-b:], np.linspace(1, 0, b))
    return sig * (e[:, None] if sig.ndim == 2 else e)
def noise(d): return rng.standard_normal(int(d * SR))
def chirp(f0, f1, d, shape=1.0):
    t = T(d); f = f0 + (f1 - f0) * (t / d) ** shape
    return np.sin(2 * np.pi * np.cumsum(f) / SR)
def reverb(sig, decay=1.2, mix=0.35):
    L = int(decay * SR); ir = rng.standard_normal(L) * np.exp(-np.arange(L) / SR * 6 / decay)
    wet = np.pad(fftconvolve(sig, ir), (0, 1))[:len(sig) + L] / np.sqrt(L) * 6
    dry = np.concatenate([sig, np.zeros(L)])
    return dry * (1 - mix) + wet * mix

VANISH = 1.75   # Menschen verschwinden

# ---------------- HOOK: Stadt-Lärm, der schlagartig verstummt ----------------
d = VANISH
traffic = filt(noise(d), hi=300) * 1.6 + filt(noise(d), 300, 2000) * 0.25
murmur = filt(noise(d), 250, 1400) * (0.6 + 0.4 * np.sin(2 * np.pi * 3.1 * T(d)) * np.sin(2 * np.pi * 1.7 * T(d)))
city = fade(traffic * 0.5 + murmur * 0.45, 0.02, 0.012)
add(0, np.stack([city, np.roll(city, 800)], 1), 0.5)
for t0, f in [(0.35, 410), (1.05, 360)]:            # Hupen
    tt = T(0.32); horn = np.sign(np.sin(2 * np.pi * f * tt)) * 0.5 + np.sign(np.sin(2 * np.pi * f * 1.26 * tt)) * 0.5
    add(t0, fade(filt(horn, 200, 2500), 0.01, 0.04), 0.12, pan=0.35 if f > 400 else 0.7)
# "Einsaugen": rückwärts anschwellendes Rauschen bis zum Verschwinden
sw = filt(noise(0.9), 800, 9000) * (T(0.9) / 0.9) ** 3
add(VANISH - 0.9, sw, 0.35)
# tiefer Sub-Drop beim Verschwinden + Stille-Ton (Tinnitus)
add(VANISH, chirp(90, 25, 1.2) * np.exp(-T(1.2) * 2.5), 0.7)
add(VANISH, fade(np.sin(2 * np.pi * 6200 * T(1.3)), 0.01, 0.9) * 0.6, 0.05)

# ---------------- 1 TAG: Strom-Brummen, Flackern, Stromausfall, Wasser ----------------
off = v(9.4)   # Straßenlaternen aus = Strom komplett weg
d = off - B[1]
tt = T(d)
hum = (np.sin(2 * np.pi * 50 * tt) + 0.5 * np.sin(2 * np.pi * 100 * tt) + 0.3 * np.sin(2 * np.pi * 150 * tt)) * np.clip(tt / 0.5, 0, 1)
add(B[1], hum, 0.07)
for _ in range(26):                                   # Knistern / Funken beim Flackern
    t0 = rng.uniform(v(5.0), off)
    add(t0, filt(noise(0.04), 2000, 9000) * np.exp(-T(0.04) * 90), rng.uniform(0.1, 0.25), pan=rng.uniform(0.2, 0.8))
# Power-Down: Generator läuft aus
pd = chirp(160, 18, 1.6, 0.6) * np.exp(-T(1.6) * 1.8)
add(off - 0.15, pd + 0.5 * chirp(320, 36, 1.6, 0.6) * np.exp(-T(1.6) * 2.2), 0.5)
add(off, filt(noise(0.25), hi=400) * np.exp(-T(0.25) * 14), 0.8)       # "Klonk"
# Wasser aus den Gullis
w0, w1 = v(8.6), B[2]
flow = fade(filt(noise(w1 - w0), 150, 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * T(w1 - w0))), 0.6, 0.4)
add(w0, flow, 0.25)
for _ in range(30):
    t0 = rng.uniform(w0, w1 - 0.1); f0 = rng.uniform(300, 700)
    add(t0, chirp(f0, f0 * 2.4, 0.06, 2) * np.exp(-T(0.06) * 40), 0.12, pan=rng.uniform(0.2, 0.8))

# ---------------- 1 WOCHE: Sirene, Geigerzähler, Grillen, Wolfsheulen ----------------
s0, s1 = B[2] + 0.5, B[3] - 0.2
tt = T(s1 - s0)
siren = np.sin(2 * np.pi * np.cumsum(750 + 220 * np.sin(2 * np.pi * 0.45 * tt)) / SR)
siren = filt(fade(siren, 0.8, 0.5), 300, 3000)
add(s0, reverb(siren, 1.5, 0.6), 0.09)
t = s0                                                 # Geigerzähler, immer schneller
while t < s1:
    rate = 3 + 22 * ((t - s0) / (s1 - s0)) ** 1.5
    t += rng.exponential(1 / rate)
    add(t, filt(noise(0.006), 1500, 8000) * np.exp(-T(0.006) * 600), 0.35, pan=0.62)
for k in np.arange(B[2] + 0.2, B[3] - 0.3, 0.9):     # Grillen
    for j in range(3):
        add(k + j * 0.06, np.sin(2 * np.pi * 4300 * T(0.04)) * np.hanning(int(0.04 * SR)), 0.05, pan=0.25)
howl_t = B[2] + 4.6                                    # Hund/Wolf heult in der Ferne
tt = T(2.2); f = 480 + 260 * np.sin(np.pi * np.clip(tt / 1.6, 0, 1)) ** 0.7 + 6 * np.sin(2 * np.pi * 5 * tt)
howl = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)
add(howl_t, reverb(fade(howl, 0.3, 0.8), 2.0, 0.55), 0.07, pan=0.3)

# ---------------- 1 JAHR: Wind, Vögel, aufplatzender Asphalt ----------------
def wind(t0, t1, g):
    d = t1 - t0; tt = T(d)
    wn = filt(noise(d), 200, 1200) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.21 * tt + 1) * np.sin(2 * np.pi * 0.13 * tt))
    add(t0, fade(np.stack([wn, np.roll(wn, 3000)], 1), 0.8, 0.8), g)
wind(B[3], B[5], 0.22)
def bird(t0, pan):
    for j in range(rng.integers(2, 5)):
        f0 = rng.uniform(2500, 4200); d = rng.uniform(0.05, 0.11)
        c = chirp(f0, f0 * rng.uniform(1.2, 1.6), d, 0.5) * np.hanning(int(d * SR))
        add(t0 + j * rng.uniform(0.09, 0.14), c, 0.07, pan)
for _ in range(14): bird(rng.uniform(B[3] + 0.3, B[4] - 0.5), rng.uniform(0.1, 0.9))
for _ in range(7): bird(rng.uniform(B[4], B[5] - 0.5), rng.uniform(0.1, 0.9))
for t0 in [B[3] + 1.4, B[3] + 3.2, B[3] + 5.3]:      # Asphalt reißt
    crack = np.pad(filt(noise(0.18), 1500, 10000) * np.exp(-T(0.18) * 30), (0, int(0.3 * SR) - int(0.18 * SR))) + filt(noise(0.3), hi=250) * np.exp(-T(0.3) * 12) * 1.5
    add(t0, crack, 0.45, pan=rng.uniform(0.3, 0.7))

# ---------------- 100 JAHRE: Grollen, Einstürze, Krähen, Flügelschlag ----------------
rum = filt(noise(B[5] - B[4]), hi=90) * 3
add(B[4], fade(rum, 1.0, 1.5), 0.35)
for i, t0 in enumerate([B[4] + 1.2, B[4] + 2.6, B[4] + 4.0, B[4] + 5.6]):
    d = 2.2; tt = T(d)
    crash = filt(noise(d), hi=500) * np.exp(-tt * 2.2) * 2 + chirp(70, 28, d) * np.exp(-tt * 2.5) * 1.2
    for _ in range(40):                                # Trümmer
        k = rng.uniform(0.05, 1.6); L = int(0.03 * SR); j = int(k * SR)
        crash[j:j + L] += filt(noise(0.03), 1200, 7000) * np.exp(-T(0.03) * 120) * np.exp(-k * 1.5) * 1.4
    add(t0, reverb(crash, 1.8, 0.4), 0.5 - i * 0.05, pan=[0.3, 0.7, 0.45, 0.6][i])
fl0 = v(30.5)
for k in np.arange(fl0, min(v(38.5), B[5]), 0.13):     # Flügelschlag des Vogelschwarms
    add(k, filt(noise(0.07), 300, 2500) * np.hanning(int(0.07 * SR)), 0.08, pan=0.8 - 0.6 * (k - fl0) / 7)
def caw(t0, pan):
    d = 0.32; tt = T(d); f = 520 - 200 * tt / d
    saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
    add(t0, fade(filt(saw, 700, 2600) + 0.2 * filt(noise(d), 800, 3000), 0.02, 0.08), 0.12, pan)
for t0, p in [(B[4] + 1.8, 0.75), (B[4] + 2.2, 0.75), (B[4] + 6.4, 0.3)]: caw(t0, p)

# ---------------- UI: Pop bei jeder Texteinblendung, Ding beim Kommentar-Button ----------------
def pop(t0, g=0.25):
    add(t0, chirp(300, 900, 0.07, 0.5) * np.exp(-T(0.07) * 45), g)
    add(t0 - 0.12, filt(noise(0.15), 2000, 8000) * (T(0.15) / 0.15) ** 2, g * 0.5)
for (a, b), facts in zip(zip(SB[1:5], SB[2:6]), [(1.5, 5.0), (1.5, 5.0), (1.5, 5.0), (1.5, 5.2)]):
    for f in facts: pop(v(a + f))
lt = lambda x: v(SB[5] + x)
for x in (0.1, 0.4, 0.58, 0.76): pop(lt(x), 0.2)
ding = sum(np.sin(2 * np.pi * f * T(1.2)) * np.exp(-T(1.2) * dk) for f, dk in [(1318, 4), (1975, 6), (2637, 8)])
add(lt(1.4), ding / 3, 0.25)

out *= np.clip((DUR - np.arange(n) / SR) / 0.8, 0, 1)[:, None]
out = np.tanh(out)
pcm = (out / max(1e-9, np.max(np.abs(out))) * 0.95 * 32767).astype(np.int16)
with wave.open(sys.argv[1] if len(sys.argv) > 1 else 'sfx.wav', 'wb') as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())
print('ok')
