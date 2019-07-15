import sys

"""
The Hack assembler reads as input a text file named Prog.asm, containing a Hack
assembly program, and produces as output a text file named Prog.hack, containing
the translated Hack machine code. The name of the input file is supplied to the
assembler as a command line argument:

prompt> Assembler Prog.asm

The translation of each individual assembly command to its equivalent binary instruction
is direct and one-to-one. Each command is translated separately. In particular,
each mnemonic component (field) of the assembly command is translated into
its corresponding bit code according to the tables in section 6.2.2, and each symbol in
the command is resolved to its numeric address as specified in section 6.2.3.
We propose an assembler implementation based on four modules: a Parser module that parses the input,
a Code module that provides the binary codes of all the assembly mnemonics,
a SymbolTable module that handles symbols,
and a main program that drives the entire translation process.
"""

class Parser:
    """Encapsulates access to the input code. Reads an assembly language command, parses it,
    and provides convenient access to the command’s components (fields and symbols).
    In addition, removes all white space and comments."""

    def __init__(self, file_name):
        """Open the file at file_name and prepare to parse it
        Generate a stream instance to use in other methods"""
        pass

    def has_more_commands(self):
        """Returns true if the stream is not empty"""
        pass

    def advance(self):
        """Reads the next command from the input and makes it the current
        command. Should be called only
        if hasMoreCommands() is true.
        Initially there is no current command"""
        pass

    def command_type(self):
        """Returns the type of the current command:
        A_COMMAND for @Xxx where Xxx is either a symbol or a decimal number
        C_COMMAND for dest=comp;jump
        L_COMMAND for (Xxx) where Xxx is a symbol."""
        pass

    def symbol(self):
        """ Returns the symbol or decimal Xxx of the current command
        @Xxx or (Xxx). Should be called only when commandType() is
        A_COMMAND or L_COMMAND."""
        pass

    def dest(self):
        """Returns the dest mnemonic in the current C-command
        (8 possibilities). Should be called only
        when commandType() is C_COMMAND"""
        pass

    def comp(self):
        """ Returns the comp mnemonic in the current C-command (28 possibilities).
        Should be called only when commandType() is C_COMMAND."""
        pass

    def jump(self):
        """Returns the jump mnemonic in the current C-command (8 possibilities).
        Should be called only when commandType() is C_COMMAND."""
        pass

    class Code:
        """Translates Hack assembly language mnemonics into binary codes."""

        @staticmethod
        def dest(mnemonic):
            """Returns the binary code of the dest mnemonic (3 bits)."""
            pass

        @staticmethod
        def comp(mnemonic):
            """Returns the binary code of the comp mnemonic (7 bits.)"""
            pass

        @staticmethod
        def jump(mnemonic):
            """Returns the binary code of the jump mnemonic (3 bits)."""
            pass

    class SymbolTable:
        """Keeps a correspondence between symbolic labels and numeric addresses."""

        def __init__(self):
            """Creates a new empty symbol table"""
            pass

        def add_pair(self, symbol, address):
            """Adds the pair (symbol, address) to the table."""

        def contains(self, symbol):
            """Does the symbol table contain the given symbol?"""
            pass

        def get_address(self, symbol):
            """Returns the address associated with the symbol."""
            pass

def main():
    parser = Parser(sys.argv[1])
    print(parser.has_more_commands())

if __name__ == "__main__":
    main()
