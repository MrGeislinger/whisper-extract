#!/usr/bin/env bash

SERIES_DIR="$1"
PLAYLIST="$2"
EXT="$3"

RAW_DIR="$SERIES_DIR/raw_data"
BEGIN=`date +'%Y%m%d-%H:%M:%S'`
echo "Download started at $BEGIN"
# Makes the directories for output when needed
yt-dlp \
     -x \
    --audio-format mp3 \
    --output "$RAW_DIR/%(uploader)s%(title)s.%(upload_date)s.%(id)s.%(ext)s" \
    $PLAYLIST
END=`date +'%Y%m%d-%H:%M:%S'`
echo "Download completed at $END"
