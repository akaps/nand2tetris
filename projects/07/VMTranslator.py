import sys
from enum import Enum
from pathlib import Path

COMMENT  = '//'
NEWLINE = '\n'

ADD = 'add'
SUB = 'sub'
NEG = 'neg'
EQUAL = 'eq'
GREATER = 'gt'
LESS = 'lt'
AND = 'and'
OR = 'or'
NOT = 'not'
PUSH = 'push'
POP = 'pop'

CONSTANT = 'constant'
LOCAL = 'local'
ARGUMENT = 'argument'
THIS = 'this'
THAT = 'that'
TEMP = 'temp'
POINTER = 'pointer'

SEGMENTS = {
    LOCAL :     '@LCL',
    ARGUMENT :  '@ARG',
    THIS :      '@THIS',
    THAT :      '@THAT',
    TEMP :      '@5',
    POINTER :   '@3'
}

class CommandType(Enum):
    ARITHMETIC = 0
    PUSH = 1
    POP = 2
    LABEL = 3
    GOTO = 4
    IF = 5
    FUNCTION = 6
    RETURN = 7
    CALL = 8

class Parser:
    '''
    Handles the parsing of a single .vm file by reading each VM command and parsing it into its lexical components
    '''
    def __init__(self, file_name):
        '''
        Prepares to parse the input vm lines
        '''
        file = open(file_name, 'r')
        self.lines = self.strip_lines(file.readlines())
        file.close()
        self.next_line = 0
        self.current_line = None

    def strip_lines(self, lines):
        result = []
        for line in lines:
            line = line.strip()
            if COMMENT in line:
                comment_index = line.index(COMMENT)
                line = line[:comment_index].strip()
            if line:
                result.append(line)
        return result

    def has_more_commands(self):
        '''
        Returns true if there are more commands in the input
        '''
        return self.next_line < len(self.lines)

    def advance(self):
        '''
        Reads the next command from the input and makes it the current command
        '''
        self.current_line = self.lines[self.next_line].split()
        self.next_line += 1

    def command_type(self):
        '''
        Returns a constant representing the type of the current command
        '''
        command = self.current_line[0]
        if command in [ADD, SUB, NEG, EQUAL, LESS, GREATER, AND, OR, NOT]:
            return CommandType.ARITHMETIC
        elif command == PUSH:
            return CommandType.PUSH
        elif command == POP:
            return CommandType.POP
        else:
            assert False, 'Unsupported type for command {cmd}'.format(cmd=self.current_line[0])

    def arg1(self):
        '''
        Returns the first argument of the current command. In the case of C_ARITHMETIC, the command (add, sub, ...) is returned instead
        Should not be called if the type is C_RETURN
        '''
        if self.command_type() == CommandType.ARITHMETIC:
            return self.current_line[0]
        return self.current_line[1]

    def arg2(self):
        '''
        Returns the second argument of the current command. Should only be called for the command types:
            C_PUSH
            C_POP
            C_FUNCTION
            C_CALL
        '''
        return self.current_line[2]

class CodeWriter:
    '''
    Generates the assembly code from parsed VM Commands
    '''
    def __init__(self, out_file_name):
        '''
        Prepares the output file to write into
        '''
        self.file = open(out_file_name, 'w')
        self.file_name = None
        self.unique_id = 0

    def set_file_name(self, file_name):
        '''
        Informs the code writer that the translation of a new VM file is started
        '''
        self.file_name = file_name

    def generate_label(self, label):
        '''
        returns a label in the form file.function$target
        '''
        pass

    def generate_unique_label(self, comp):
        '''
        returns a label in the form comp$####
        '''
        result = '{comp}${num}'.format(comp=comp, num=self.unique_id)
        self.unique_id += 1
        return result

    def write_arithmetic(self, command):
        '''
        Writes to the output file the assembly code that implements the given arithmetic command
        '''
        OPERAND = {
            ADD :       'M=D+M',
            SUB :       'M=M-D',
            NEG :       'M=-M',
            LESS :      'D;JLT',
            EQUAL :     'D;JEQ',
            GREATER :   'D;JGT',
            AND :       'M=D&M',
            OR :        'M=D|M',
            NOT :       'M=!M'
        }

        if command in [NEG, NOT]:
            self.decrement_stack()
            self.write_line(OPERAND[command])
            self.increment_stack()
        elif command in [ADD, SUB, AND, OR]:
            self.pop_D_register()
            self.decrement_stack()
            self.write_line(OPERAND[command])
            self.increment_stack()
        elif command in [LESS, EQUAL, GREATER]:
            self.pop_D_register()
            IS_TRUE = self.generate_unique_label('{cmd}_TRUE'.format(cmd=command))
            IS_FALSE = self.generate_unique_label('{cmd}_FALSE'.format(cmd=command))
            DONE = self.generate_unique_label('{cmd}_DONE'.format(cmd=command))
            self.decrement_stack()
            self.write_line('D=M-D')
            self.write_line('@{jump}'.format(jump=IS_TRUE))
            self.write_line(OPERAND[command])
            self.write_line('({false})'.format(false=IS_FALSE))
            self.write_line('@0')
            self.write_line('D=A')
            self.write_line('@{jump}'.format(jump=DONE))
            self.write_line('0;JMP')
            self.write_line('({true})'.format(true=IS_TRUE))
            self.write_line('@0')
            self.write_line('D=A-1')
            self.write_line('({done})'.format(done=DONE))
            self.push_D_register()
        else:
            assert False, 'unsupported arithmetic expression {expr}'.format(expr=command)

    def write_push_pop(self, cmd_type, segment, index):
        '''
        Writes to the output file the assembly code that implements the given push/pop command
        '''
        if cmd_type == CommandType.PUSH:
            self.push(segment, index)
        if cmd_type == CommandType.POP:
            self.pop(segment, index)

    def push(self, segment, index):
        if segment == CONSTANT:
            self.write_line('@{index}'.format(index=index))
            self.write_line('D=A')
            self.push_D_register()
        elif segment in [LOCAL, ARGUMENT, THIS, THAT]:
            self.calculate_address(segment, index)
            self.write_line('D=M')
            self.push_D_register()
        elif segment in [TEMP, POINTER]:
            self.calculate_offset(segment, index)
            self.write_line('D=M')
            self.push_D_register()
        else:
            assert False, 'unsupported segment {segment}'.format(segment=segment)

    def pop(self, segment, index):
        if segment in [LOCAL, ARGUMENT, THIS, THAT]:
            self.calculate_address(segment, index)
            self.store_at_address()
        elif segment in [TEMP, POINTER]:
            self.calculate_offset(segment, index)
            self.store_at_address()
        else:
            assert False, 'unsupported segment {segment}'.format(segment=segment)

    def store_at_address(self):
        self.write_line('@R13')
        self.write_line('M=D')
        self.decrement_stack()
        self.write_line('D=M')
        self.write_line('@R13')
        self.write_line('A=M')
        self.write_line('M=D')

    def calculate_address(self, segment, index):
        self.write_line(SEGMENTS[segment])
        self.write_line('A=M')
        self.write_line('D=A')
        self.write_line('@{index}'.format(index=index))
        self.write_line('AD=D+A')

    def calculate_offset(self, segment, index):
        self.write_line(SEGMENTS[segment])
        self.write_line('D=A')
        self.write_line('@{index}'.format(index=index))
        self.write_line('AD=D+A')

    def write_line(self, line):
        self.file.write(line)
        self.file.write(NEWLINE)

    def decrement_stack(self):
        self.write_line('@SP')
        self.write_line('AM=M-1')

    def increment_stack(self):
        self.write_line('@SP')
        self.write_line('M=M+1')

    def pop_D_register(self):
        self.decrement_stack()
        self.write_line('D=M')

    def push_D_register(self):
        self.write_line('@SP')
        self.write_line('A=M')
        self.write_line('M=D')
        self.increment_stack()

    def close(self):
        '''
        Closes the output file
        '''
        self.file.close()

def translate(parser, writer):
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == CommandType.ARITHMETIC:
            writer.write_arithmetic(parser.arg1())
        elif parser.command_type() in [CommandType.PUSH, CommandType.POP]:
            writer.write_push_pop(parser.command_type(), parser.arg1(), parser.arg2())
        else:
            assert False, 'Unsupported line {cmd}'.format(cmd=parser.current_line)

def main():
    path = Path(sys.argv[1])
    parser = Parser(path)
    out_file_name = '{stem}.asm'.format(stem=path.stem)
    writer = CodeWriter(path.parent.joinpath(out_file_name))

    translate(parser, writer)

    writer.close()

if __name__ == '__main__':
    main()
