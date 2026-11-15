# Spracherkennung (Whisper small via sherpa-onnx) für hochgeladene Sprecher-Aufnahmen.
# Usage: python3 stt.py <whisper-ordner> <aufnahme_16k_mono.wav> "0-9.9,9.9-17"   (Abschnitte in Sekunden)
import sys, wave, numpy as np, sherpa_onnx
d = sys.argv[1]; wav = sys.argv[2]; segs = [tuple(map(float, s.split('-'))) for s in sys.argv[3].split(',')]
rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{d}/small-encoder.int8.onnx", decoder=f"{d}/small-decoder.int8.onnx", tokens=f"{d}/small-tokens.txt", language="de", task="transcribe", num_threads=4)
w = wave.open(wav); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; sr = w.getframerate()
for a, b in segs:
    s = rec.create_stream(); s.accept_waveform(sr, x[int(a * sr):int(b * sr)]); rec.decode_stream(s)
    print(f"{a:6.2f}-{b:6.2f}: {s.result.text.strip()}")
