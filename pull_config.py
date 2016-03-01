#!/usr/bin/env python2.7
__author__ = 'Cameron Childress'
__email__ = ''.join(['c', __author__.split()[1].lower(), '@', 'rallydev.com'])

import base64
import datetime
import json
import os
import requests
import sys

from lib_io import (get_config_from_file,
                    get_config_from_switch,
                    run_ssh_commands)
from output_buffer import Output_buffer

# Fill these in
owner = ''
repo = ''
branch = ''
author = ''
email = ''

console_logs = Output_buffer('pull-console.log')
debug_logs = Output_buffer('pull-debug.log')

def build_json(hostname, config_file, sha):
    commit_timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d_%H:%M:%S')
    commit_log = hostname + '_' + commit_timestamp
    config_combined = '\n'.join(config_file)
    payload = {
        'message':commit_log,
        'committer':{
            'name':author,
            'email':email
            },
        'content':base64.b64encode('\n'.join(config_file)),
        'branch':branch
    }
    if sha:
        payload['sha'] = sha
    return payload

def check_for_sha(hostname):
    headers, get_path = github_setup(hostname)
    get_path += '?ref={}'.format(branch)
    response = requests.get(get_path, headers=headers)
    if response.status_code == 200:
        sha = json.loads(response.text)['sha']
    else:
        sha = None
    return sha

def find_hostname(config_file):
    hostname = None
    for line in config_file:
        if 'hostname' in line:
            hostname = line.split(' ')[1]
    return hostname

def push_github(hostname, payload):
    headers, put_path = github_setup(hostname)
    response = requests.put(put_path, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        console_logs.append('Config data updated for {}.'.format(hostname))
    elif response.status_code == 201:
        console_logs.append('Created new config file for {}.'.format(hostname))
    else:
        console_logs.append("Failure to upload config data for {} to Github.".format(hostname))
        debug_logs.append('HTTP response code for {}: {}'.format(hostname, response.status_code))
        debug_logs.append('json data dump:')
        debug_logs.append(json.dumps(payload))

def github_setup(hostname):
    try:
        token = os.environ['OAUTH']
    except KeyError:
        console_logs.append("Fatal - oauth key missing.")
        return None
    headers = {'Authorization':"token {}".format(token),
               'Accept':'application/vnd.github.v3+json'}
    content_path = 'https://api.github.com/repos/{}/{}/contents/{}'.format(owner, repo, hostname)
    return headers, content_path

def main(argv):
    # Check to make sure we actually have the data we need before connecting to anything
    if len(argv) != 4:
        console_logs.append(("Fatal - There are either too few or too many arguments supplied.\n"
                             "This program expects exactly three arguments:\n"
                             "  hostname - the hostname or IP address of the target\n"
                             "  username - the username with which to connect\n"
                             "  password - the password with which to connect"))
        console_logs.console_out()
        return(1)
    target = argv[1]
    username = argv[2]
    password = argv[3]

    current_config = get_config_from_switch(target, username, password)
    if current_config:
        console_logs.append("Current configuration read from {}:".format(target))
        console_logs.append(current_config)
        console_logs.append('-------------------------------')
    else:
        debug_logs.write_out()
        return(1)

    hostname = find_hostname(current_config)
    if hostname:
        console_logs.append('Detected hostname: "{}""'.format(hostname))
    else:
        console_logs.append("Could not detect hostname.")
        debug_logs.write_out()
        return(1)
    sha = check_for_sha(hostname)
    payload = build_json(hostname, current_config, sha)
    push_github(hostname, payload)

    if debug_logs:
        debug_logs.write_out()
    console_logs.write_out()
    console_logs.console_out()
    return(0)

if __name__ == '__main__':
    main(sys.argv)
