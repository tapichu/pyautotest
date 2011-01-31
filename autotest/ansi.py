# -*- coding: utf-8 -*-
"""
Utility functions to wrap strings in ANSI colour codes.
"""

from sys import stdout

def highlight(string, is_tty=stdout.isatty()):
    """
    Green text.
    """
    return ('\033[32;1m' + string + '\033[0m') if is_tty else string

def error(string, is_tty=stdout.isatty()):
    """
    Red text.
    """
    return ('\033[31;1m' + string + '\033[0m') if is_tty else string

