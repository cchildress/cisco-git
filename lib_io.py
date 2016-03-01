from Exscript import Account
from Exscript.protocols import SSH2

def get_config_from_file(config_file):
    try:
        with open(config_file) as f:
            new_config = f.readlines()
    except IOError as e:
        console_logs.append("Fatal - Could not open file '{}' to read new config.".format(config_file))
        debug_logs.append(e)
        console_logs.console_out()
        return(None)
    return new_config

def get_config_from_switch(target, username, password):
    result = run_ssh_commands(target, username, password, ['show running-config'])
    if result:
        old_config = result[0][1:-2]
    else:
        old_config = None
    return old_config

def run_ssh_commands(target, username, password, commands):
    results = []
    account = Account(username, password)
    conn = SSH2()
    conn.connect(target)
    conn.login(account)
    for command in commands:
        conn.execute(command)
        response = conn.response
        response = response.replace('\r', '').split('\n')
        results.append(response)
    conn.send('exit')
    conn.close()
    return results
