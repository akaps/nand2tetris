import sys
from pathlib import Path
from enum import Enum

SEGMENTS = {
    'local' : 'LCL',
    'argument' : 'ARG',
    'this' : 'THIS',
    'that' : 'THAT',
    'pointer' : 'THIS',
    'temp' : 'TEMP'
}

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

COMMANDS = {
    'add'       : CmdType.C_ARITHMETIC,
    'sub'       : CmdType.C_ARITHMETIC,
    'neg'       : CmdType.C_ARITHMETIC,
    'eq'        : CmdType.C_ARITHMETIC,
    'gt'        : CmdType.C_ARITHMETIC,
    'lt'        : CmdType.C_ARITHMETIC,
    'and'       : CmdType.C_ARITHMETIC,
    'or'        : CmdType.C_ARITHMETIC,
    'not'       : CmdType.C_ARITHMETIC,
    'push'      : CmdType.C_PUSH,
    'pop'       : CmdType.C_POP,
    'label'     : CmdType.C_LABEL,
    'goto'      : CmdType.C_GOTO,
    'if-goto'   : CmdType.C_IF,
    'function'  : CmdType.C_FUNCTION,
    'call'      : CmdType.C_CALL,
    'return'    : CmdType.C_RETURN
}

VM_EXTENSION = '.vm'
ASSEMBLY_EXTENSION = '.asm'
STACK_START = 0x100
HEAP_START = 0x800

#commonly used delimeters
COMMENT = '//'

class Parser:
    '''
    Handles the parsing of a single .vm file by reading each VM command and parsing it into its lexical components
    '''
    def __init__(self, file_name):
        '''
        Prepares to parse the input vm lines
        '''
        file = open(file_name, 'r')
        self.lines = self.remove_decorators(file.readlines())
        file.close()
        self.next_command = 0
        self.current_command = None

    def remove_decorators(self, lines):
        result = []
        for line in lines:
            line=line.strip()
            if COMMENT in line:
                comment_index= line.index(COMMENT)
                line = line[:comment_index]
            if line:
                result.append(line.strip().split())
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
        return COMMANDS[self.arg1]

    def arg1(self):
        '''
        Returns the first argument of the current command. In the case of C_ARITHMETIC, the command (add, sub, ...) is returned
        Should not be called if the type is C_RETURN
        '''
        return self.current_command[0]

    def arg2(self):
        '''
        Returns the second argument of the current command. Should only be called for the command types:
            C_PUSH
            C_POP
            C_FUNCTION
            C_CALL
        '''
        return int(self.current_command[1])

class CodeWriter:
    '''
    Generates the assembly code from parsed VM Commands
    '''
    def __init__(self, out_file_name):
        '''
        Prepares the output file to write into
        '''
        self.file = open(out_file_name, 'w')

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
        self.file.close()

def translate(parser, writer):
    while parser.has_more_commands():
        parser.advance()
        print(parser.current_command)
        print('^{arg1}'.format(arg1=parser.arg1()))

def translate_files(files, write_name):
    writer = CodeWriter(write_name)
    for file_name in files:
        print('parsing {file}'.format(file=file_name))
        parser = Parser(file_name)
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

    print('translating {files}->{output}'.format(
        files=files,
        output=write_name
    ))

    translate_files(files, write_name)

if __name__ == '__main__':
    main()
