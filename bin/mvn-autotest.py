#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if __name__ == '__main__':
    sys.path.append('../')
    from autotest.realtime import gen_follow_all
    from autotest.maven import gen_mvntest

    # TODO: check if mvn command is available (subprocess.check_call(['mvn', 'clean'])?)
    
    # TODO: use argparse to create a command line interface
    modified_files = gen_follow_all('*.java', sys.argv[1])
    results = gen_mvntest(modified_files, sys.argv[1])

    for exit_code, output in results:
        # Stop the program if we're unable to execute the command
        if 0 < exit_code > 1:
            modified_files.close()
        else:
            if exit_code == 1:
                print 'Errors in the tests!\n'

            lines = output.splitlines()[-18:]
            for line in lines:
                print line

