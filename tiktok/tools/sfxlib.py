# Bausteine für synthetisierte Soundeffekte (keine Samples nötig). Wird von den sfx.py der Folgen importiert.
import numpy as np, wave
from scipy.signal import butter, sosfilt, fftconvolve
SR = 44100
rng = np.random.default_rng(42)

class Track:
    def __init__(self, dur):
        self.dur = dur; self.n = int(SR * dur); self.out = np.zeros((self.n, 2))
    def add(self, t0, sig, gain=1.0, pan=0.5):
        i0 = int(t0 * SR)
        if i0 >= self.n: return
        if sig.ndim == 1: sig = np.stack([sig * np.sqrt(1 - pan), sig * np.sqrt(pan)], 1)
        if i0 < 0: sig = sig[-i0:]; i0 = 0
        m = min(len(sig), self.n - i0); self.out[i0:i0 + m] += sig[:m] * gain
    def save(self, path):
        o = self.out * np.clip((self.dur - np.arange(self.n) / SR) / 0.8, 0, 1)[:, None]
        o = np.tanh(o); pcm = (o / max(1e-9, np.max(np.abs(o))) * 0.95 * 32767).astype(np.int16)
        with wave.open(path, 'wb') as wf:
            wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())
        print('wrote', path)

def T(d): return np.arange(int(d * SR)) / SR
def noise(d): return rng.standard_normal(int(d * SR))
def filt(x, lo=None, hi=None, order=4):
    if lo and hi: sos = butter(order, [lo, hi], 'bandpass', fs=SR, output='sos')
    elif lo: sos = butter(order, lo, 'highpass', fs=SR, output='sos')
    else: sos = butter(order, hi, 'lowpass', fs=SR, output='sos')
    return sosfilt(sos, x)
def fade(sig, fi=0.05, fo=0.05):
    L = len(sig); e = np.ones(L); a, b = int(fi * SR), int(fo * SR)
    if a: e[:a] = np.linspace(0, 1, a)
    if b: e[-b:] = np.minimum(e[-b:], np.linspace(1, 0, b))
    return sig * (e[:, None] if sig.ndim == 2 else e)
def chirp(f0, f1, d, shape=1.0):
    t = T(d); f = f0 + (f1 - f0) * (t / d) ** shape
    return np.sin(2 * np.pi * np.cumsum(f) / SR)
def reverb(sig, decay=1.2, mix=0.35):
    L = int(decay * SR); ir = rng.standard_normal(L) * np.exp(-np.arange(L) / SR * 6 / decay)
    wet = np.pad(fftconvolve(sig, ir), (0, 1))[:len(sig) + L] / np.sqrt(L) * 6
    return np.concatenate([sig, np.zeros(L)]) * (1 - mix) + wet * mix
def stereo(sig, delay=0.02): return np.stack([sig, np.roll(sig, int(delay * SR))], 1)

# --- fertige Effekte ---
def pop(tr, t0, g=0.25):
    tr.add(t0, chirp(300, 900, 0.07, 0.5) * np.exp(-T(0.07) * 45), g)
    tr.add(t0 - 0.12, filt(noise(0.15), 2000, 8000) * (T(0.15) / 0.15) ** 2, g * 0.5)
def ding(tr, t0, g=0.25):
    d = sum(np.sin(2 * np.pi * f * T(1.2)) * np.exp(-T(1.2) * k) for f, k in [(1318, 4), (1975, 6), (2637, 8)])
    tr.add(t0, d / 3, g)
def whoosh_in(tr, t_end, d=0.9, g=0.35):
    tr.add(t_end - d, filt(noise(d), 800, 9000) * (T(d) / d) ** 3, g)
def sub_drop(tr, t0, g=0.7, d=1.2): tr.add(t0, chirp(90, 25, d) * np.exp(-T(d) * 2.5), g)
def boom(tr, t0, g=0.8, d=2.5):
    tt = T(d); f = 25 + 70 * np.exp(-tt * 6)
    tr.add(t0, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 1.4) + filt(noise(d), hi=200) * np.exp(-tt * 5), g)
def wind(tr, t0, t1, g=0.22, lo=200, hi=1200, howl=False):
    d = t1 - t0; tt = T(d)
    wn = filt(noise(d), lo, hi) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.21 * tt + 1) * np.sin(2 * np.pi * 0.13 * tt))
    if howl: wn += 0.25 * np.sin(2 * np.pi * np.cumsum(500 + 180 * np.sin(2 * np.pi * 0.3 * tt)) / SR) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.17 * tt))
    tr.add(t0, fade(stereo(wn, 0.07), 0.8, 0.8), g)
def bird(tr, t0, pan=0.5, g=0.07):
    for j in range(rng.integers(2, 5)):
        f0 = rng.uniform(2500, 4200); d = rng.uniform(0.05, 0.11)
        tr.add(t0 + j * rng.uniform(0.09, 0.14), chirp(f0, f0 * rng.uniform(1.2, 1.6), d, 0.5) * np.hanning(int(d * SR)), g, pan)
def crack(tr, t0, g=0.45, pan=0.5):
    c = np.pad(filt(noise(0.18), 1500, 10000) * np.exp(-T(0.18) * 30), (0, int(0.3 * SR) - int(0.18 * SR))) + filt(noise(0.3), hi=250) * np.exp(-T(0.3) * 12) * 1.5
    tr.add(t0, c, g, pan)
def ice_crack(tr, t0, g=0.5, pan=0.5):
    """tiefes, singendes Eis-Knacken (wie auf einem zufrierenden See)"""
    d = 1.4; tt = T(d)
    pew = chirp(2400, 300, d, 0.4) * np.exp(-tt * 3.5) * 0.5
    snap = np.pad(filt(noise(0.05), 2000, 10000) * np.exp(-T(0.05) * 80), (0, len(tt) - int(0.05 * SR)))
    tr.add(t0, reverb(pew + snap, 1.5, 0.5), g, pan)
def crickets(tr, t0, t1, g=0.05, pan=0.25):
    for k in np.arange(t0, t1, 0.9):
        for j in range(3): tr.add(k + j * 0.06, np.sin(2 * np.pi * 4300 * T(0.04)) * np.hanning(int(0.04 * SR)), g, pan)
def heartbeat(tr, t0, t1, bpm=70, g=0.5):
    for k in np.arange(t0, t1, 60 / bpm):
        for off, a in [(0, 1.0), (0.18, 0.7)]:
            tt = T(0.25); tr.add(k + off, np.sin(2 * np.pi * np.cumsum(60 * np.exp(-tt * 8) + 35) / SR) * np.exp(-tt * 14) * a, g)
def tick_fast(tr, t0, t1, rate0=4, rate1=14, g=0.35):
    t = t0; j = 0
    while t < t1:
        L = int(0.025 * SR); s = (rng.standard_normal(L) * 0.3 + np.sin(2 * np.pi * (2400 if j % 2 else 1800) * np.arange(L) / SR)) * np.exp(-np.arange(L) / (0.005 * SR))
        tr.add(t, s, g, 0.65 if j % 2 else 0.35)
        t += 1 / lerp(rate0, rate1, (t - t0) / (t1 - t0)); j += 1
def bubbles(tr, t0, t1, count=30, g=0.12):
    for _ in range(count):
        t = rng.uniform(t0, t1 - 0.1); f0 = rng.uniform(300, 700)
        tr.add(t, chirp(f0, f0 * 2.4, 0.06, 2) * np.exp(-T(0.06) * 40), g, rng.uniform(0.2, 0.8))
def underwater(tr, t0, t1, g=0.4):
    d = t1 - t0; s = filt(noise(d), hi=350) * 2 + 0.3 * np.sin(2 * np.pi * 48 * T(d))
    tr.add(t0, fade(stereo(s, 0.05), 0.4, 0.4), g)
def lerp(a, b, k): return a + (b - a) * min(1, max(0, k))
