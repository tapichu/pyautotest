# -*- coding: utf-8 -*-
"""
Generators for searching for files, getting their stat information,
their last modification time, etc.
"""

import os
import os.path
import fnmatch

MTIME = 'st_mtime'
PATH = 'path'

COLNAMES = ('st_mode', 'st_ino', 'st_dev', 'st_nlink', 'st_uid', 'st_gid',
        'st_size', 'st_atime', 'st_mtime', 'st_ctime', 'path')

def gen_find(file_pattern, top_dir):
    for path, dir_list, file_list in os.walk(top_dir):
        for name in fnmatch.filter(file_list, file_pattern):
            yield os.path.join(path, name)

def gen_filestat(fileseq):
    tuples = (os.stat(file) + (file,) for file in fileseq)
    info = (dict(zip(COLNAMES, t)) for t in tuples)
    return info

def gen_mtimes(fileseq):
    return (dict({PATH: file, MTIME: os.path.getmtime(file)}) for file in fileseq)

