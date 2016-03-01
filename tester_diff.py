#!/usr/bin/env python2.7
__author__ = 'Cameron Childress'
__email__ = ''.join(['c', __author__.split()[1].lower(), '@', 'rallydev.com'])

import sys

from lib_config_diff import (build_changes,
                             cleanup_config,
                             config_to_seq,
                             negate_line)

def main(argv):
    # Check to make sure we actually have the data we need before connecting to anything
    if len(argv) != 3:
        print("Fatal - There are either too few or too many arguments supplied.\n"
              "This program expects exactly two arguments:\n"
              "  before - the existing config\n"
              "  after - the new config")
        return(1)
    before = argv[1]
    after = argv[2]

    with open(before) as f:
        old_config = f.readlines()
    with open(after) as f:
        new_config = f.readlines()
    new_config = cleanup_config(new_config)
    old_config = cleanup_config(old_config)
    new_parsed = config_to_seq(new_config)
    old_parsed = config_to_seq(old_config)
    changes = build_changes(old_parsed, new_parsed)
    print("Changes:")
    for change in changes:
        print(change)

if __name__ == '__main__':
    main(sys.argv)
