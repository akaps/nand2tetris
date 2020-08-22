'''
Emits VM commands into a file
'''
class VMWriter:
    def __init__(self, out_name):
        '''
        Creates a new file and prepares it for writing VM commands
        '''
        self.file = open(out_name, 'w')

    def write_line(self, line):
        self.file.write(line + '\n')

    def write_push(self, segment, index):
        '''
        Writes a VM push command
        '''
        self.write_line('push {seg} {index}'.format(seg=segment, index=index))

    def write_pop(self, segment, index):
        '''
        Writes a VM pop command
        '''
        self.write_line('pop {seg} {index}'.format(seg=segment, index=index))

    def write_arithmetic(self, command):
        '''
        Writes a VM arithmetic command
        '''
        self.write_line(command)

    def write_label(self, label):
        '''
        Writes a VM label command
        '''
        self.write_line(label)

    def write_goto(self, label):
        '''
        Writes a VM goto command
        '''
        self.write_line('goto {label}'.format(label=label))

    def write_if(self, label):
        '''
        Writes a VM if-goto command
        '''
        self.write_line('if-goto {label}'.format(label=label))

    def write_call(self, name, n_args):
        '''
        Writes a VM call command
        '''
        self.write_line('call {name} {args}'.format(name=name, args=n_args))

    def write_function(self, name, n_locals):
        '''
        Writes a VM function command
        '''
        self.write_line('function {name} {n_locals}'.format(name=name, n_locals=n_locals))

    def write_return(self):
        '''
        Writes a VM return command
        '''
        self.write_line('return')

    def close(self, ):
        '''
        closes the output file
        '''
        self.file.close()
