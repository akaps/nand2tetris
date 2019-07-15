import sys
import os
import re
from enum import Enum

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

class CommandType(Enum):
    ADDRESS = 0
    COMPUTE = 1
    LOAD = 2

class Parser:
    """Encapsulates access to the input code. Reads an assembly language command, parses it,
    and provides convenient access to the command’s components (fields and symbols).
    In addition, removes all white space and comments."""

    def __init__(self, lines):
        """Open the file at file_name and prepare to parse it
        Generate a stream instance to use in other methods"""
        self.lines = lines
        self.next_line = 0
        self.current_command = None

    def has_more_commands(self):
        """Returns true if the stream is not empty"""
        return self.next_line < len(self.lines)

    def advance(self):
        """Reads the next command from the input and makes it the current
        command. Should be called only
        if hasMoreCommands() is true.
        Initially there is no current command"""
        self.current_command = self.lines[self.next_line]

    def command_type(self):
        """Returns the type of the current command:
        A_COMMAND for @Xxx where Xxx is either a symbol or a decimal number
        C_COMMAND for dest=comp;jump
        L_COMMAND for (Xxx) where Xxx is a symbol."""
        if "@" in self.current_command:
            return CommandType.ADDRESS
        elif "(" in self.current_command:
            return CommandType.LOAD
        else:
            return CommandType.COMPUTE

    def symbol(self):
        """ Returns the symbol or decimal Xxx of the current command
        @Xxx or (Xxx). Should be called only when commandType() is
        A_COMMAND or L_COMMAND."""
        if self.command_type() == CommandType.ADDRESS:
            return self.current_command[1:]
        else:
            return self.current_command[1:-1]

    #Reminder that Compute instructions take the form of Dest=Comp;Jump
    def dest(self):
        """Returns the dest mnemonic in the current C-command
        (8 possibilities). Should be called only
        when commandType() is C_COMMAND"""
        return re.match(r"\w(?==)", self.current_command)[0]

    def comp(self):
        """ Returns the comp mnemonic in the current C-command (28 possibilities).
        Should be called only when commandType() is C_COMMAND."""
        return re.match(r"(?<==)\w(?=;)", self.current_command)[0]

    def jump(self):
        """Returns the jump mnemonic in the current C-command (8 possibilities).
        Should be called only when commandType() is C_COMMAND."""
        return re.match(r"(?<=;)\w", self.current_command)[0]

    class Code:
        """Translates Hack assembly language mnemonics into binary codes."""

        @staticmethod
        def dest(mnemonic):
            """Returns the binary code of the dest mnemonic (3 bits)."""
            res = 0
            if "A" in mnemonic:
                res += 0b100
            if "M" in mnemonic:
                res += 0b001
            if "D" in mnemonic:
                res += 0b010
            return "{res}".format(res=res, type=bin)

        @staticmethod
        def comp(mnemonic):
            """Returns the binary code of the comp mnemonic (7 bits.)"""
            a = "1" if "M" in mnemonic else "0"
            mnemonic = mnemonic.replace("M", "A")
            computation = {
                "0"   : "101010",
                "1"   : "111111",
                "-1"  : "111010",
                "D"   : "001100",
                "A"   : "110000",
                "!D"  : "001101",
                "!A"  : "110001",
                "-D"  : "001111",
                "-A"  : "110011",
                "D+1" : "011111",
                "A+1" : "110111",
                "D-1" : "001110",
                "A-1" : "110010",
                "D+A" : "000010",
                "D-A" : "010011",
                "A-D" : "000111",
                "D&A" : "000000",
                "D|A" : "010101"
            }
            return a + computation[mnemonic]

        @staticmethod
        def jump(mnemonic):
            """Returns the binary code of the jump mnemonic (3 bits)."""
            jumpcode = {
                None  : "000",
                "JGT" : "001",
                "JEQ" : "010",
                "JGE" : "011",
                "JLT" : "100",
                "JNE" : "101",
                "JLE" : "110",
                "JMP" : "111"
            }
            return jumpcode[mnemonic]

    class SymbolTable:
        """Keeps a correspondence between symbolic labels and numeric addresses."""

        def __init__(self):
            """Creates a new empty symbol table"""
            self.symbols = {}
            self.add_pair("SP", 0x0000)
            self.add_pair("LCL", 0x0001)
            self.add_pair("ARG", 0x0002)
            self.add_pair("THIS", 0x0003)
            self.add_pair("THAT", 0x0004)
            for i in range(16):
                register = "R{num}".format(num=i)
                self.add_pair(register, 0x0000 + i)
            self.add_pair("SCREEN", 0x4000)
            self.add_pair("KBD", 0x6000)
            self.next_label = 0x0010

        def add_pair(self, symbol, address):
            """Adds the pair (symbol, address) to the table."""
            self.symbols[symbol] = address

        def contains(self, symbol):
            """Does the symbol table contain the given symbol?"""
            return symbol in self.symbols

        def get_address(self, symbol):
            """Returns the address associated with the symbol."""
            return self.symbols[symbol]

def main():
    #initialize the assembler
    file_name = sys.argv[1]
    lines = open(file_name, "r").readlines()
    parser = Parser(lines)

    #perform the translation
    print(parser.has_more_commands())

    #output results to file
    name, ext = os.path.basename(file_name).split(".")
    ext = 'hack'
    print("created file {name}.{ext}".format(name=name, ext=ext))

if __name__ == "__main__":
    main()
