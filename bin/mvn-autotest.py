#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import optparse

def option_parser():
    parser = optparse.OptionParser()
    parser.add_option('-p', '--path', type='string', dest='root_path',
            help='path to the directory that contains the POM',
            metavar='PATH')
    parser.add_option('-l', '--lines', type='int', dest='lines', default=24,
            help='limit the number of lines shown for test error reports')
    return parser

if __name__ == '__main__':

    sys.path.append('../')

    from autotest.ansi import error
    from autotest.maven import gen_mvntest, report_totals, report_errors
    from autotest.realtime import gen_follow_all

    # Parse arguments
    parser = option_parser()
    (options, args) = parser.parse_args()
    if not options.root_path:
        parser.error('option -p is mandatory')

    modified_files = gen_follow_all('*.java', options.root_path)
    results = gen_mvntest(modified_files, options.root_path)

    for clazz, exit_code, output in results:
        # Stop the program if we're unable to execute the command
        if 0 < exit_code > 1:
            modified_files.close()
        else:
            # Print the number of tests, errors, etc.
            report_totals(output)

            if exit_code == 1:
                print error('\nErrors in the tests!\n')
                report_errors(clazz, output, options.lines)

