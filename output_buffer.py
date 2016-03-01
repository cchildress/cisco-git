class Output_buffer(list):
    '''
    This is a class to manage logging both to files and the console.
    It inherits from list so you can use append() to add entries to the buffer.

    Inputs:
        target - The filename to which the buffer will be written.
                 Specify this if you plan to use the write_out() method.

     Methods:
     console_out() - Write the current buffer to the running shell.
     write_out() - Write the current buffer to the target specified.
                   This will fail with an error to the console if the target is missing.
     '''
    def __init__(self, target=None):
        self._target = target
        list.__init__(self)
    def console_out(self):
        for entry in self:
            if isinstance(entry, list):
                for line in entry:
                    print(line)
            else:
                print(entry)
    def write_out(self):
        if self._target:
            with open(self._target, 'wb') as f:
                for entry in self:
                    output = entry
                    if isinstance(entry, list):
                        for line in entry:
                            output = '\n'.join([x for x in entry])
                    if isinstance(entry, str):
                        output = entry.rstrip()
                    f.write('{}\n'.format(output))
        else:
            print('Cannot write output logs - no target specified.')
