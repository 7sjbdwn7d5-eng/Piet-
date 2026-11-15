# Synthesizes the soundtrack (no samples needed): drone pad, clock ticks, whooshes and impacts.
import numpy as np, wave, sys
SR = 44100; DUR = 44.0
n = int(SR * DUR); t = np.arange(n) / SR
out = np.zeros((n, 2))
rng = np.random.default_rng(7)
CUTS = [3.6, 12.2, 20.8, 29.8, 39.2]
SCENES = [(0, 3.6), (3.6, 12.2), (12.2, 20.8), (20.8, 29.8), (29.8, 39.2), (39.2, 44)]
note = lambda m: 440 * 2 ** ((m - 69) / 12)
CHORDS = [[45, 52, 57, 60], [45, 52, 57, 60, 64], [38, 45, 50, 53, 56], [41, 48, 53, 57, 60], [45, 52, 57, 60, 64, 67], [48, 55, 60, 64, 67]]

def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); acc = 0.0
    # vectorised one-pole via lfilter-like recursion in chunks
    from itertools import accumulate
    y = np.array(list(accumulate(x * (1 - a), lambda p, v: p * a + v)))
    return y

def env(t0, t1, fade=0.6):
    e = np.clip((t - t0) / fade, 0, 1) * np.clip((t1 - t) / fade, 0, 1)
    return e

# pad
for (a, b), ch in zip(SCENES, CHORDS):
    e = env(a - 0.3, b + 0.3, 0.5)
    sig = np.zeros(n)
    for m in ch:
        f = note(m)
        for det in (-0.12, 0.12):
            ff = f * 2 ** (det / 12)
            sig += np.sin(2 * np.pi * ff * t) + 0.35 * np.sin(4 * np.pi * ff * t) + 0.15 * np.sin(6 * np.pi * ff * t)
    lfo = 0.75 + 0.25 * np.sin(2 * np.pi * 0.25 * t)
    sig *= e * lfo / len(ch)
    out[:, 0] += sig * 0.16; out[:, 1] += np.roll(sig, 300) * 0.16
# sub bass pulse (heartbeat-ish) during scenes
beat = 0.5
for k in np.arange(3.6, 39.2, beat):
    i0 = int(k * SR); L = int(0.35 * SR); tt = np.arange(L) / SR
    f = 55 * np.exp(-tt * 6) + 38
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9) * 0.32
    out[i0:i0 + L] += s[:, None]
# clock ticks (alternating tick/tock), faster in the 100-year scene
ticks = list(np.arange(3.6, 29.8, 0.5)) + list(np.arange(29.8, 39.2, 0.25))
for j, k in enumerate(ticks):
    i0 = int(k * SR); L = int(0.03 * SR)
    noise = rng.standard_normal(L) * np.exp(-np.arange(L) / (0.004 * SR))
    tone = np.sin(2 * np.pi * (2400 if j % 2 else 1800) * np.arange(L) / SR) * np.exp(-np.arange(L) / (0.006 * SR))
    s = (noise * 0.25 + tone * 0.35) * 0.5
    pan = 0.7 if j % 2 else 0.3
    out[i0:i0 + L, 0] += s * (1 - pan); out[i0:i0 + L, 1] += s * pan
# whoosh before each cut + impact on cut
for c in CUTS:
    L = int(0.9 * SR); i0 = int((c - 0.8) * SR); tt = np.arange(L) / SR
    nz = rng.standard_normal(L)
    # crude rising band: highpass-ish by differencing lowpassed noise with rising cutoff
    lp = lowpass(nz, 1500); hp = nz - lp
    e = (tt / 0.8) ** 2 * np.clip((0.9 - tt) / 0.1, 0, 1)
    w = (lp * 0.6 + hp * 0.4) * e * 0.5
    out[i0:i0 + L, 0] += w; out[i0:i0 + L, 1] += np.roll(w, 200)
    L2 = int(1.6 * SR); j0 = int(c * SR); tt2 = np.arange(L2) / SR
    f = 30 + 90 * np.exp(-tt2 * 12)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt2 * 2.5) * 0.9
    crack = lowpass(rng.standard_normal(L2), 3000) * np.exp(-tt2 * 18) * 0.8
    seg = boom + crack
    m = min(L2, n - j0); out[j0:j0 + m] += seg[:m, None]
# hook: riser 0-2.1 then "vanish" shimmer
L = int(2.1 * SR); tt = np.arange(L) / SR
f = 200 + 800 * (tt / 2.1) ** 2
riser = np.sin(2 * np.pi * np.cumsum(f) / SR) * (tt / 2.1) ** 2 * 0.25
out[:L] += riser[:, None]
for k in range(40):
    st = 2.1 + rng.uniform(0, 1.2); i0 = int(st * SR); L = int(0.5 * SR); tt = np.arange(L) / SR
    s = np.sin(2 * np.pi * rng.uniform(1500, 4500) * tt) * np.exp(-tt * 8) * 0.06
    p = rng.uniform(0, 1); out[i0:i0 + L, 0] += s * (1 - p); out[i0:i0 + L, 1] += s * p
# final fade
out *= np.clip((DUR - t) / 1.2, 0, 1)[:, None]
out = np.tanh(out * 1.2)
out /= np.max(np.abs(out)) * 1.02
pcm = (out * 32767).astype(np.int16)
with wave.open(sys.argv[1] if len(sys.argv) > 1 else 'soundtrack.wav', 'wb') as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())
print('ok')
