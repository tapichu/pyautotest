# -*- coding: utf-8 -*-
"""
Generator for running unit tests with Apache Maven
"""

import os
import re
import subprocess
import time

from autotest.ansi import highlight, error

STATS_PAT = r"""[\w ]+\:\s(\d+),\s   # total
        \w+\:\s(\d+),\s              # failures
        \w+\:\s(\d+),\s              # errors
        \w+\:\s(\d+),\s              # skipped
        [\w ]+\:\s([0-9.]+) \w+      # elapsed time"""
STATS_PATC = re.compile(STATS_PAT, re.VERBOSE)

def gen_mvntest(fileseq, root_dir):
    """
    Tries to execute tests for every file in fileseq.
    root_dir should point to the directory where maven's POM can be found.
    """
    if not root_dir.endswith(os.sep):
        root_dir = root_dir + os.sep

    for f in fileseq:
        # TODO: handle projects with and without submodules
        project, clazz = get_submodule_and_class(f, root_dir)
        command = create_command(project, clazz)

        result = run_command(command, root_dir)

        yield result

def get_submodule_and_class(path, root_dir):
    """
    Returns a tuple with the name of the class and the
    name of the project / submodule the class belongs to
    """
    relative_path = path[len(root_dir):]
    parts = relative_path.split(os.sep)
    project = parts[0]
    clazz = parts[-1][:-5]   # Remove the .java extension

    return (project, clazz)

def create_command(project, clazz):
    """
    Builds the maven command to execute the tests
    """
    # TODO: This are just some hard-coded conventions.
    #       It would be better to make this "configurable" or even better,
    #       search the uses of this class and loop for @Test annotations.
    if clazz.endswith('Test'):
        cmd = 'mvn -pl %s -am test -Dtest=%s' % (project, clazz)
    elif clazz.endswith('IT'):  # failsafe-maven-plugin for integration tests
        cmd = 'mvn -pl %s -am verify -Dit.test=%s' % (project, clazz)
    else:
        if clazz.endswith('Impl'):
            clazz = clazz[:-4] + '*'
        test = clazz + 'Test'
        it = clazz + 'IT'
        cmd = 'mvn -pl %s -am verify -Dtest=%s -Dit.test=%s' % (project, test, it)

    return cmd

def run_command(command, root_dir):
    """
    Runs a command using subprocess
    """
    print highlight('\nRunning tests: %s' % command)

    start_time = time.time()
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, cwd=root_dir)
    stdout_value, stderr_value = proc.communicate()
    end_time = time.time()

    if 0 < proc.returncode > 1:
        print error('Error trying to run the tests')
        print error(stderr_value)
        stdout_value = stderr_value
    else:
        print highlight('------------------------------')
        print highlight('Finished tests in %.2f seconds\n' % (end_time - start_time))

    return (proc.returncode, stdout_value)

def report_totals(output):
    """
    Report the number of tests run, errors, etc.
    """
    groups = (STATS_PATC.match(line) for line in output.splitlines())
    tuples = (g.groups() for g in groups if g)

    results = [0,0,0,0,0]
    for t in tuples:
        results[0] += int(t[0])     # total
        results[1] += int(t[1])     # failures
        results[2] += int(t[2])     # errors
        results[3] += int(t[3])     # skipped
        results[4] += float(t[4])   # elapsed time

    print 'Tests run: %d, Failures: %d, Errors: %d, Skipped: %d, '\
            'Time elapsed: %f' % tuple(results)

