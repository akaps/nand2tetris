import sys
import os
from enum import Enum

class CommandType(Enum):
    C_ARITHMETIC = 0,
    C_PUSH = 1,
    C_POP = 2,
    C_LABEL = 3,
    C_GOTO = 4,
    C_IF = 5,
    C_FUNCTION = 6,
    C_RETURN = 7
    C_CALL = 8

class Parser:
    """
    Handles the parsing of a single .vm file by reading each VM command and parsing it into its lexical components
    """
    def __init__(self, lines):
        """
        Prepares to parse the input vm lines
        """
        pass

    def has_more_commands(self):
        """
        Returns true if there are more commands in the input
        """
        pass

    def advance(self):
        """
        Reads the next command from the input and makes it the current command
        """
        pass

    def command_type(self):
        """
        Returns a constant representing the type of the current command
        """
        pass

    def arg1(self):
        """
        Returns the first argument of the current command. In the case of C_ARITHMETIC, the command (add, pop, ...) is returned
        Should not be called if the type is C_RETURN
        """
        pass

    def arg2(self):
        """
        Returns the second argument of the current command. Should only be called for the command types:
            C_PUSH
            C_POP
            C_FUNCTION
            C_CALL
        """
        pass

class CodeWriter:
    """
    Generates the assembly code from parsed VM Commands
    """
    def __init__(self, out_file_name):
        """
        Preparaes the output file to write into
        """
        pass

    def write_araithmetic(self, command):
        """
        Writes to the output file the assembly code that implements the given arithmetic command
        """
        pass

    def write_push_pop(self, cmd_type, segment, index):
        """
        Writes to the output file the assembly code that implements the given push/pop command
        """
        pass

    def close(self):
        """
        Closes the output file
        """
        pass

def translate(from_file, to_file):
    pass

def main():
    #read from file
    read_name = sys.argv[1]
    name, _ = os.path.basename(read_name).split('.')
    write_name = "{dir}{sep}{name}{ext}".format(
        dir=os.path.dirname(read_name),
        sep=os.sep,
        name=name,
        ext='.asm')

    #perform the translation
    translate(read_name, write_name)
    print("Successfully translated {file} to {output}".format(
        file=os.path.basename(read_name),
        output=write_name))

if __name__ == '__main__':
    main()
