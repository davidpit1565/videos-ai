#!/bin/sh
# usage: check_v5.sh <video.mp4> [cues.json]  : ffprobe, loudness, freezedetect, frame-difference vs ep 82, safecheck
HERE=$(cd "$(dirname "$0")" && pwd); export PATH=/opt/ffmpeg7/bin:$PATH; V=$1
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt,sample_rate,channels,duration -of compact "$V"
ffmpeg -hide_banner -nostats -i "$V" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|LRA|Peak):"
echo "freezedetect:"; ffmpeg -hide_banner -nostats -i "$V" -vf freezedetect=n=-45dB:d=0.5 -an -f null - 2>&1 | grep -c freeze_start
python3 "$HERE/metric.py" "$V" /home/user/videos-ai/studio/public/reels/reel-82.mp4
cd /root/lemo-opuscar && node "$HERE/safecheck.mjs" "$HERE" 2>&1 | grep -v -e optional -e WebGL | tail -3
