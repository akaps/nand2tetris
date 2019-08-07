def UNFINISHED(method):
    assert False, 'Unfinished method {name}'.format(name=method.__name__)

'''
Emits VM commands into a file
'''
class VMWriter:

    def __init__(self, out_file):
        '''
        Creates a new file and prepares it for writing VM commands
        '''
        self.file = open(out_file, 'w')
        self.write_line('remove me when fully implemented')

    def write_line(self, line):
        self.file.write(line)
        self.file.write('\n')

    def write_push(self, segment, index):
        '''
        Writes a VM push command
        '''
        UNFINISHED(self.write_push)

    def write_pop(self, segment, index):
        '''
        Writes a VM pop command
        '''
        UNFINISHED(self.write_pop)

    def write_arithmetic(self, command):
        '''
        Writes a VM arithmetic command
        '''
        UNFINISHED(self.write_arithmetic)

    def write_label(self, label):
        '''
        Writes a VM goto command
        '''
        UNFINISHED(self.write_label)

    def write_goto(self, label):
        '''
        Writes a VM label command
        '''
        UNFINISHED(self.write_goto)

    def write_if(self, label):
        '''
        Writes a VM If-goto command
        '''
        UNFINISHED(self.write_if)

    def write_call(self, name, n_args):
        '''
        Writes a VM call command
        '''
        UNFINISHED(self.write_call)

    def write_function(self, name, n_locals):
        '''
        Writes a VM function command
        '''
        UNFINISHED(self.write_function)

    def write_return(self):
        '''
        Writes a VM return command
        '''
        UNFINISHED(self.write_return)

    def close(self):
        '''
        Closes the output file
        '''
        self.file.close()
