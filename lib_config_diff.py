from ignore_lines import ignore_flat, ignore_regex

def build_changes(old, new):
    changes = []
    todo_list = []
    for entry in old:
        if not entry in new:
            max_depth = sorted(entry.keys())[-1]
            negated = negate_line(entry[max_depth])
            entry[max_depth] = negated
            todo_list.append(entry)
    for entry in new:
        if not entry in old:
            todo_list.append(entry)
    for seq in todo_list:
        for idx in sorted(seq.keys()):
            changes.append(seq[idx])
    if changes:
        changes.insert(0, 'configure terminal')
        changes.append('end')
    return changes

def cleanup_config(lines):
    middle_stage = []
    clean_config = []
    for line in lines:
        if line.rstrip() not in ignore_flat:
            middle_stage.append(line.rstrip())
    for line in middle_stage:
        if not any(pattern.match(line) for pattern in ignore_regex):
            clean_config.append(line)
    return clean_config

def config_to_seq(config_in):
    command_seq = []
    scope_struct = {}
    for line in config_in:
        scope = len(line) - len(line.lstrip(' '))
        if scope == 0:
            scope_struct = {}
        scope_struct[scope] = line
        command_seq.append(dict(scope_struct))
    return command_seq

def negate_line(line):
    line = line.lstrip(' ')
    if line[:2] == 'no':
        line = line[3:]
    else:
        line = 'no {}'.format(line)
    return line
