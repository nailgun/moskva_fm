#!/bin/sh

for file in $@; do
    ffmpeg -i $file -f s16le -acodec pcm_s16le - 2> /dev/null
done
