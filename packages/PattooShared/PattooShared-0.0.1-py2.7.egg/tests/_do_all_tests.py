#!/usr/bin/env python3
"""Script to test all the pattoo-shared unittests.

1)  This script runs each unittest script in the test directory.

2)  The only scripts run in the module are those whose names
    start with 'test_'

3)  All unittest scripts must be able to successfully run independently
    of all others.

"""

from __future__ import print_function
import locale
import os
import sys
import subprocess
import argparse

# Try to create a working PYTHONPATH
TEST_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
ROOT_DIRECTORY = os.path.abspath(os.path.join(TEST_DIRECTORY, os.pardir))
if TEST_DIRECTORY.endswith('/pattoo-shared/tests') is True:
    sys.path.append(ROOT_DIRECTORY)
else:
    print(
        'This script is not installed in the "pattoo-shared/tests" directory. '
        'Please fix.')
    sys.exit(2)

# pattoo-shared libraries
from tests.dev import unittest_setup
from tests.dev import error_code_report
from pattoo_shared import files


def main():
    """Test all the pattoo-shared modules with unittests.

    Args:
        None

    Returns:
        None

    """
    # Set up parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', help='', action='store_true')
    args = parser.parse_args()

    # Determine unittest directory
    root_dir = ROOT_DIRECTORY
    test_dir = '{}/tests'.format(root_dir)

    # Run the test
    command = 'python3 -m unittest discover --start {}'.format(test_dir)
    if args.verbose is True:
        command = '{} --verbose'.format(command)
    run_script(command)

    # Check error codes
    error_code_report.check()

    # Print
    message = ('\nHooray - All Done OK!\n')
    print(message)


def run_script(cli_string):
    """Run the cli_string UNIX CLI command and record output.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    encoding = locale.getdefaultlocale()[1]
    pattoo_returncode = ('----- pattoo-shared Return Code '
                         '----------------------------------------')
    pattoo_stdoutdata = ('----- pattoo-shared Test Output '
                         '----------------------------------------')
    pattoo_stderrdata = ('----- pattoo-shared Test Error '
                         '-----------------------------------------')

    # Say what we are doing
    string2print = '\nRunning Command: {}'.format(cli_string)
    print(string2print)

    # Run update_devices script
    do_command_list = list(cli_string.split(' '))

    # Create the subprocess object
    process = subprocess.Popen(
        do_command_list,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdoutdata, stderrdata = process.communicate()
    returncode = process.returncode

    # Crash if the return code is not 0
    if returncode != 0:
        # Print the Return Code header
        string2print = '\n{}'.format(pattoo_returncode)
        print(string2print)

        # Print the Return Code
        string2print = '\n{}'.format(returncode)
        print(string2print)

        # Print the STDOUT header
        string2print = '\n{}\n'.format(pattoo_stdoutdata)
        print(string2print)

        # Print the STDOUT
        for line in stdoutdata.decode(encoding).split('\n'):
            string2print = '{}'.format(line)
            print(string2print)

        # Print the STDERR header
        string2print = '\n{}\n'.format(pattoo_stderrdata)
        print(string2print)

        # Print the STDERR
        for line in stderrdata.decode(encoding).split('\n'):
            string2print = '{}'.format(line)
            print(string2print)

        # All done
        sys.exit(2)


if __name__ == '__main__':
    # Test the configuration variables
    unittest_setup.ready()

    # Do the unit test
    main()
