import re
ignore_flat = ['',
               '!',
               'Building configuration...']

ignore_regex = [re.compile(r'Current configuration : \d+ bytes'),
                re.compile(r'version.*'),
                re.compile(r'^.*!')]
