import sys
from pathlib import Path
from enum import Enum

VM_EXTENSION = '.vm'
ASSEMBLY_EXTENSION = '.asm'

#commonly used delimeters
COMMENT = '//'
NEWLINE = '\n'

class CmdType(Enum):
    C_ARITHMETIC = 0 #form: add/sub/neg/eq/gt/lt/and/or/not
    C_PUSH = 1 #form: push segment index. push value of segment[index] to stack
    C_POP = 2 #form: pop segment index. pop topmost stack element and store in segment[index]
    C_LABEL = 3 #label for goto
    C_GOTO = 4 #unconditional branching
    C_IF = 5 #conditional branching
    C_FUNCTION = 6 #form: functionName nLocals. includes number of variables
    C_RETURN = 7 #transfer control back to calling function
    C_CALL = 8 #form: call functionName nArgs

ADD         = 'add'
SUB         = 'sub'
NEG         = 'neg'
EQ          = 'eq'
GT          = 'gt'
LT          = 'lt'
AND         = 'and'
OR          = 'or'
NOT         = 'not'
PUSH        = 'push'
POP         = 'pop'
LABEL       = 'label'
GOTO        = 'goto'
IF          = 'if-goto'
FUNCTION    = 'function'
CALL        = 'call'
RETURN      = 'return'

COMMAND_TYPES = {
    ADD         : CmdType.C_ARITHMETIC,
    SUB         : CmdType.C_ARITHMETIC,
    NEG         : CmdType.C_ARITHMETIC,
    EQ          : CmdType.C_ARITHMETIC,
    GT          : CmdType.C_ARITHMETIC,
    LT          : CmdType.C_ARITHMETIC,
    AND         : CmdType.C_ARITHMETIC,
    OR          : CmdType.C_ARITHMETIC,
    NOT         : CmdType.C_ARITHMETIC,
    PUSH        : CmdType.C_PUSH,
    POP         : CmdType.C_POP,
    LABEL       : CmdType.C_LABEL,
    GOTO        : CmdType.C_GOTO,
    IF          : CmdType.C_IF,
    FUNCTION    : CmdType.C_FUNCTION,
    CALL        : CmdType.C_CALL,
    RETURN      : CmdType.C_RETURN
}

CONSTANT    = 'constant'
LOCAL       = 'local'
ARGUMENT    = 'argument'
THIS        = 'this'
THAT        = 'that'
POINTER     = 'pointer'
TEMP        = 'temp'

SEGMENTS = {
    LOCAL     : 'LCL',
    ARGUMENT  : 'ARG',
    THIS      : 'THIS',
    THAT      : 'THAT',
    POINTER   : 3,
    TEMP      : 5
}

class Parser:
    '''
    Handles the parsing of a single .vm file by reading each VM command and parsing it into its lexical components
    '''
    def __init__(self, file_name):
        '''
        Prepares to parse the input vm lines
        '''
        file = open(file_name, 'r')
        self.lines = self.preprocess(file.readlines())
        file.close()
        self.next_command = 0
        self.current_command = None

    def preprocess(self, lines):
        result = []
        for line in lines:
            line=line.strip()
            if COMMENT in line:
                comment_index= line.index(COMMENT)
                line = line[:comment_index]
            if line:
                line = line.strip().split()
                for index, element in enumerate(line):
                    if element.isdigit():
                        line[index] = int(element)
                result.append(line)

        return result

    def has_more_commands(self):
        '''
        Returns true if there are more commands in the input
        '''
        return self.next_command < len(self.lines)

    def advance(self):
        '''
        Reads the next command from the input and makes it the current command
        '''
        self.current_command = self.lines[self.next_command]
        self.next_command += 1

    def command_type(self):
        '''
        Returns a constant representing the type of the current command
        '''
        return COMMAND_TYPES[self.current_command[0]]

    def arg1(self):
        '''
        Returns the first argument of the current command. In the case of C_ARITHMETIC, the command (add, sub, ...) is returned instead
        Should not be called if the type is C_RETURN
        '''
        if self.command_type() == CmdType.C_ARITHMETIC:
            return self.current_command[0]
        return self.current_command[1]

    def arg2(self):
        '''
        Returns the second argument of the current command. Should only be called for the command types:
            C_PUSH
            C_POP
            C_FUNCTION
            C_CALL
        '''
        return int(self.current_command[2])

class CodeWriter:
    '''
    Generates the assembly code from parsed VM Commands
    '''
    def __init__(self, out_file_name):
        '''
        Prepares the output file to write into
        '''
        self.file = open(out_file_name, 'w')
        self.labels = []

    def set_file_name(self, file_name):
        path = Path(file_name)
        self.file_name, _ = path.name.split('.')

    def generate_label(self, id):
        result = '{file}.{id}'.format(file=self.file_name, id=id)
        if type(id) is not int:
            i = 1
            while result in self.labels:
                result = '{file}.{id}.{num}'.format(file=self.file_name, id=id, num=i)
                i += 1
            self.labels.append(result)
        return result

    def write_arithmetic(self, command):
        '''
        Writes to the output file the assembly code that implements the given arithmetic command
        '''
        OP_LINE = {
            ADD : 'M=D+M',
            SUB : 'M=M-D',
            NEG : 'M=-M',
            AND : 'M=D&M',
            OR  : 'M=D|M',
            NOT : 'M=!M',
            EQ  : 'D;JEQ',
            GT  : 'D;JGT',
            LT  : 'D;JLT'
        }
        if command in [ADD, SUB, NEG, AND, OR, NOT]:
            self.write_decrement_sp()
            if command in [NEG, NOT]:
                self.write_line(OP_LINE[command])
            else:
                self.write_line('D=M')
                self.write_decrement_sp()
                self.write_line(OP_LINE[command])
        elif command in [EQ, GT, LT]:
            COMP_TRUE = self.generate_label('{cmd}_TRUE'.format(cmd=command))
            COMP_DONE = self.generate_label('{cmd}_DONE'.format(cmd=command))
            self.write_load_comparison(COMP_TRUE)
            self.write_line(OP_LINE[command])
            self.write_push_true_false(COMP_DONE, COMP_TRUE)
        self.write_increment_sp()

    def write_load_comparison(self, CASE_TRUE):
        self.write_decrement_sp()
        self.write_line('D=M')
        self.write_decrement_sp()
        self.write_line('D=M-D')
        self.write_line('@{label}'.format(label=CASE_TRUE))

    def write_push_true_false(self, CASE_DONE, CASE_TRUE):
        self.write_line('@0')
        self.write_line('D=A')
        self.write_line('@{label}'.format(label=CASE_DONE))
        self.write_line('0;JMP')
        self.write_line('({label})'.format(label=CASE_TRUE))
        self.write_line('@0')
        self.write_line('D=A-1')
        self.write_line('({label})'.format(label=CASE_DONE))
        self.write_line('@SP')
        self.write_line('A=M')
        self.write_line('M=D')

    def write_increment_sp(self):
        '''Update the stack pointer assuming a push occurred'''
        self.write_line('@SP')
        self.write_line('M=M+1')

    def write_decrement_sp(self):
        '''Update the stack pointer assuming a pop occurred. M contains the popped value'''
        self.write_line('@SP')
        self.write_line('AM=M-1')

    def write_push_pop(self, cmd_type, segment, index):
        '''
        Writes to the output file the assembly code that implements the given push/pop command
        '''
        if cmd_type == CmdType.C_PUSH:
            self.write_push(segment, index)
        if cmd_type == CmdType.C_POP:
            self.write_pop(segment, index)

    def write_push(self, segment, index):
        if segment == CONSTANT:
            self.write_line('@{index}'.format(index=index))
            self.write_line('D=A')
        elif segment in [LOCAL, ARGUMENT, THIS, THAT]:
            self.offset_segment(segment, index)
            self.write_line('A=D')
            self.write_line('D=M')
        elif segment in [POINTER, TEMP]:
            self.offset_literal(segment, index)
            self.write_line('A=D')
            self.write_line('D=M')
        else:
            #static
            static_label=self.generate_label(index)
            self.write_line('@{label}'.format(label=static_label))
            self.write_line('D=M')
        self.write_line('@SP')
        self.write_line('A=M')
        self.write_line('M=D')
        self.write_increment_sp()

    def write_pop(self, segment, index):
        if segment in [LOCAL, ARGUMENT, THIS, THAT]:
            self.offset_segment(segment, index)
        elif segment in [POINTER, TEMP]:
            self.offset_literal(segment, index)
        else:
            #static
            static_label = self.generate_label(index)
            self.write_line('@{label}'.format(label=static_label))
            self.write_line('D=A')
        self.write_line('@SP')
        self.write_line('A=M')
        self.write_line('M=D')
        self.write_decrement_sp()
        self.write_line('D=M')
        self.write_line('@SP')
        self.write_line('A=M+1')
        self.write_line('A=M')
        self.write_line('M=D')

    def offset_literal(self, segment, index):
        self.write_line('@{seg}'.format(seg=SEGMENTS[segment]))
        self.write_line('D=A')
        self.write_line('@{index}'.format(index=index))
        self.write_line('D=D+A')

    def offset_segment(self, segment, index):
        self.write_line('@{seg}'.format(seg=SEGMENTS[segment]))
        self.write_line('D=M')
        self.write_line('@{index}'.format(index=index))
        self.write_line('D=D+A')

    def write_line(self, line):
        self.file.write(line)
        self.file.write(NEWLINE)

    def close(self):
        '''
        Closes the output file
        '''
        self.file.close()

def translate(parser, writer):
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == CmdType.C_ARITHMETIC:
            writer.write_arithmetic(parser.arg1())
        if parser.command_type() == CmdType.C_POP or parser.command_type() == CmdType.C_PUSH:
            writer.write_push_pop(parser.command_type(), parser.arg1(), parser.arg2())

def translate_files(files, write_name):
    writer = CodeWriter(write_name)
    for file_name in files:
        print('parsing {file}'.format(file=file_name))
        parser = Parser(file_name)
        writer.set_file_name(file_name)
        translate(parser, writer)
    writer.close()

def get_write_path(dir, name):
    write_path = Path(dir)
    return write_path.joinpath(name + ASSEMBLY_EXTENSION)

def main():
    path = Path(sys.argv[1])
    files = []
    write_name = ''
    if path.is_file():
        files.append(path)
        name, _ = path.name.split('.')
        write_name = get_write_path(path.parent, name)
    else:
        for file_name in path.iterdir():
            if file_name.suffix == VM_EXTENSION:
                files.append(file_name)
        write_name = get_write_path(path, path.name)
    translate_files(files, write_name)
    print('translated {files}->{output}'.format(
        files=files,
        output=write_name
    ))

if __name__ == '__main__':
    main()