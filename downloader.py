#!/usr/bin/env python
#
# usage:
# fm_dump.py station [dd.mm[.yyyy]]Thh:mm [dd.mm[.yyyy]]Thh:mm
# fm_dump.py station
#
# stations:
# 2013 - megapolis

import os
import sys
import shutil
import datetime
import tempfile

here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

def url_list(station, start, end):
    url_template = 'http://dt.moskva.fm/files/%(station)s/mp4/%(time)s.mp4'
    time_format = '%Y/%m/%d/%H%M'

    minute = datetime.timedelta(minutes=1)
    it = start
    while it < end:
        time = it.strftime(time_format)
        url = url_template % dict(
            station=station,
            time=time
        )
        yield url
        it += minute

def download_urls(urls, retry_count=10):
    dirpath = tempfile.mkdtemp('moskva_fm')
    try:
        for i,url in enumerate(urls):
            tmp,ext = os.path.splitext(url)
            filename = '%08d%s' % (i,ext)
            filepath = os.path.join(dirpath, filename)
            cmd = 'wget -O %s %s' % (filepath, url)
            success = False
            retries_left = retry_count
            while not success and retries_left > 0:
                success = os.system(cmd) == 0
                retries_left -= 1
            assert success
    except:
        shutil.rmtree(dirpath)
        raise
    return dirpath

def main():
    station = sys.argv[1]
    if len(sys.argv) == 2:
        import gui
        start, end = gui.pick_times()
    elif len(sys.argv) == 4:
        start = parse_datetime(sys.argv[2])
        end = parse_datetime(sys.argv[3])
    else:
        raise RuntimeError('invalid arguments')
    assert start < end

    dirpath = download_urls(url_list(station, start, end))
    pcm2mp3 = here('pcm2mp3.sh')
    pcmcat = here('pcmcat.sh')
    try:
        os.system('sh %s %s/* | sh %s' % (pcmcat, dirpath, pcm2mp3))
    finally:
        shutil.rmtree(dirpath)

if __name__ == '__main__':
    main()
