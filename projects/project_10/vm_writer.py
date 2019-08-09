'''
Emits VM commands into a file
'''
class VMWriter:
    def __init__(self, out_name):
        '''
        Creates a new file and prepares it for writing VM commands
        '''
        pass

    def write_push(self, segment, index):
        '''
        Writes a VM push command
        '''
        pass

    def write_pop(self, segment, index):
        '''
        Writes a VM pop command
        '''
        pass

    def write_arithmetic(self, command):
        '''
        Writes a VM arithmetic command
        '''
        pass

    def write_label(self, label):
        '''
        Writes a VM label command
        '''
        pass

    def write_goto(self, label):
        '''
        Writes a VM goto command
        '''
        pass

    def write_if(self, label):
        '''
        Writes a VM if-goto command
        '''
        pass

    def write_call(self, name, n_args):
        '''
        Writes a VM call command
        '''
        pass

    def write_function(self, name, n_locals):
        '''
        Writes a VM function command
        '''
        pass

    def write_return(self, name, n_locals):
        '''
        Writes a VM return command
        '''
        pass

    def close(self, ):
        '''
        closes the output file
        '''
        pass
