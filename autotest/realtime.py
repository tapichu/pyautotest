# -*- coding: utf-8 -*-
"""
Real-time generators (infinite sequences) for monitoring file modifications.
"""

import os.path
import time

import autotest.search as search

def gen_follow(file, sleep_time=1, lastmod=time.time()):
    while True:
        try:
            mtime = os.path.getmtime(file)
        except OSError:
            time.sleep(sleep_time)
            continue
        else:
            if mtime <= lastmod:
                time.sleep(sleep_time)
                continue
            lastmod = mtime
            yield file

def gen_follow_all(file_pattern, top_dir, sleep_time=1, lastmod=time.time()):
    while True:
        files = search.gen_find(file_pattern, top_dir)
        mtimes = search.gen_mtimes(files)
        modified = (m for m in mtimes if m[search.MTIME] > lastmod)

        # TODO: make another generator that returns lists instead of one
        #       file at a time.
        max = lastmod
        for m in modified:
            if m[search.MTIME] > max:
                max = m[search.MTIME]
            yield m[search.PATH]

        lastmod = max
        time.sleep(sleep_time)

