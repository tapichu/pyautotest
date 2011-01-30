#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if __name__ == '__main__':
    sys.path.append('../')

    from autotest.ansi import error
    from autotest.maven import gen_mvntest, report_totals
    from autotest.realtime import gen_follow_all

    # TODO: use argparse to create a command line interface
    modified_files = gen_follow_all('*.java', sys.argv[1])
    results = gen_mvntest(modified_files, sys.argv[1])

    for exit_code, output in results:
        # Stop the program if we're unable to execute the command
        if 0 < exit_code > 1:
            modified_files.close()
        else:
            # Print the number of tests, errors, etc.
            report_totals(output)

            if exit_code == 1:
                print error('\nErrors in the tests!\n')

