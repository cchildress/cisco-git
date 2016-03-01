#!/usr/bin/env python2.7
__author__ = 'Cameron Childress'
__email__ = ''.join(['c', __author__.split()[1].lower(), '@', 'rallydev.com'])

import sys

from lib_config_diff import (build_changes,
                             cleanup_config,
                             config_to_seq,
                             negate_line)
from lib_io import (get_config_from_file,
                    get_config_from_switch,
                    run_ssh_commands)
from output_buffer import Output_buffer

console_logs = Output_buffer('apply-console.log')
debug_logs = Output_buffer('apply-debug.log')

def main(argv):
    # Check to make sure we actually have the data we need before connecting to anything
    if len(argv) != 5:
        console_logs.append(("Fatal - There are either too few or too many arguments supplied.\n"
                             "This program expects exactly four arguments:\n"
                             "  hostname - the hostname or IP address of the target\n"
                             "  username - the username with which to connect\n"
                             "  password - the password with which to connect\n"
                             "  config_file - the configuration file to apply"))
        console_logs.console_out()
        return(1)
    target = argv[1]
    username = argv[2]
    password = argv[3]
    config_file = argv[4]

    new_config = get_config_from_file(config_file)
    if new_config:
        new_config = cleanup_config(new_config)
        console_logs.append("New configuration read from {}:".format(config_file))
        console_logs.append(new_config)
        console_logs.append('-------------------------------')
    else:
        debug_logs.write_out()
        return(1)
    old_config = get_config_from_switch(target, username, password)
    if old_config:
        old_config = cleanup_config(old_config)
        console_logs.append("Old configuration read from {}:".format(target))
        console_logs.append(old_config)
        console_logs.append('-------------------------------')
    else:
        debug_logs.write_out()
        return(1)

    new_parsed = config_to_seq(new_config)
    old_parsed = config_to_seq(old_config)
    changes = build_changes(old_parsed, new_parsed)
    console_logs.append("Commands that will be run:")
    console_logs.append(changes)
    console_logs.append('-------------------------------')

    if changes:
        # Actually execute the changes
        result = run_ssh_commands(target, username, password, changes)
        console_logs.append('Target device output:')
        for entry in result:
            console_logs.append(entry)
    else:
        console_logs.append("Skipped appling changes - none found")

    if debug_logs:
        debug_logs.write_out()
    console_logs.write_out()
    console_logs.console_out()
    return(0)

if __name__ == '__main__':
    main(sys.argv)
