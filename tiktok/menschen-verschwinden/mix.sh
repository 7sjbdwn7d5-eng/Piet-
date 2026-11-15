#!/usr/bin/env bash
# Endmix: Erzähler vorne; Musik, Effekte und Nachrichtenstimme ducken automatisch unter dem Erzähler.
# Usage: ./mix.sh music.wav sfx.wav news.wav voice.wav video_noaudio.mp4 out.mp4
set -e
MUSIC=$1; SFX=$2; NEWS=$3; VOICE=$4; VIDEO=$5; OUT=$6
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")
ffmpeg -y -loglevel error -i "$MUSIC" -i "$SFX" -i "$NEWS" -i "$VOICE" -filter_complex "
[3:a]apad=whole_dur=$DUR,asplit=4[v][sc1][sc2][sc3];
[0:a]volume=0.30[m];[m][sc1]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[md];
[1:a]volume=0.75[s];[s][sc2]sidechaincompress=threshold=0.05:ratio=2.5:attack=20:release=300[sd];
[2:a]apad=whole_dur=$DUR,volume=0.42[n];[n][sc3]sidechaincompress=threshold=0.03:ratio=3:attack=15:release=250[nd];
[md][sd][nd][v]amix=inputs=4:normalize=0:duration=first,alimiter=limit=0.95[a]" -map "[a]" -t "$DUR" -ar 44100 /tmp/_mix.wav
ffmpeg -y -loglevel error -i "$VIDEO" -i /tmp/_mix.wav -c:v copy -c:a aac -b:a 192k -movflags +faststart "$OUT"
rm -f /tmp/_mix.wav
echo "wrote $OUT"
