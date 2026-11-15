#!/usr/bin/env bash
# Bereitet eine fertige Sprachaufnahme (z.B. ElevenLabs-MP3 oder eigene Aufnahme) für den Mix auf.
# Usage: ./extvoice.sh <eingang.mp3> <out.wav> [versatz_s]
set -e
OFF=${3:-0}; MS=$(python3 -c "print(int(float('$OFF')*1000))")
ffmpeg -y -loglevel error -i "$1" -af "aresample=44100,highpass=f=70,acompressor=threshold=-24dB:ratio=2:attack=10:release=200,adelay=${MS}|${MS},loudnorm=I=-15:TP=-1.5" -ac 2 -ar 44100 "$2"
echo "wrote $2"
