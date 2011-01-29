# -*- coding: utf-8 -*-
"""
Generator for running unit tests with Apache Maven
"""

import os
import subprocess
import time

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
    print '\nRunning tests:', command

    start_time = time.time()
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, cwd=root_dir)
    stdout_value, stderr_value = proc.communicate()
    end_time = time.time()

    if 0 < proc.returncode > 1:
        print 'Error trying to run the tests'
        print stderr_value
        stdout_value = stderr_value
    else:
        print '----------------------------'
        print 'Finished tests in %f seconds\n' % (end_time - start_time)

    return (proc.returncode, stdout_value)

