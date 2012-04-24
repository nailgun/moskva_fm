#!/bin/sh

exec ffmpeg -f s16le -acodec pcm_s16le -ac 2 -i - -b 32k -f mp3 -acodec libmp3lame -
