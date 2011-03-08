# -*- coding: utf-8 -*-
"""
KDE notifications using kdialog
"""

import subprocess

def passive_popup(message, timeout, title=None, icon=None):
    command = 'kdialog --passivepopup "%s" %d' % (message, timeout)
    if title:
        command += ' --title "%s"' % title
    if icon:
        command += ' --icon "%s"' % icon

    subprocess.Popen(command, shell=True)

