
class Parser:
    '''
    Handles the parsing of a single .vm file by reading each VM command and parsing it into its lexical components
    '''
    def __init__(self, file_name):
        '''
        Prepares to parse the input vm lines
        '''
        pass

    def has_more_commands(self):
        '''
        Returns true if there are more commands in the input
        '''
        pass

    def advance(self):
        '''
        Reads the next command from the input and makes it the current command
        '''
        pass

    def command_type(self):
        '''
        Returns a constant representing the type of the current command
        '''
        pass

    def arg1(self):
        '''
        Returns the first argument of the current command. In the case of C_ARITHMETIC, the command (add, sub, ...) is returned instead
        Should not be called if the type is C_RETURN
        '''
        pass

    def arg2(self):
        '''
        Returns the second argument of the current command. Should only be called for the command types:
            C_PUSH
            C_POP
            C_FUNCTION
            C_CALL
        '''
        pass

class CodeWriter:
    '''
    Generates the assembly code from parsed VM Commands
    '''
    def __init__(self, out_file_name):
        '''
        Prepares the output file to write into
        '''
        pass

    def set_file_name(self, file_name):
        '''
        Informs the code writer that the translation of a new VM file is started
        '''
        pass

    def write_arithmetic(self, command):
        '''
        Writes to the output file the assembly code that implements the given arithmetic command
        '''
        pass

    def write_push_pop(self, cmd_type, segment, index):
        '''
        Writes to the output file the assembly code that implements the given push/pop command
        '''
        pass

    def close(self):
        '''
        Closes the output file
        '''
        pass

def main():
    pass

if __name__ == '__main__':
    main()
