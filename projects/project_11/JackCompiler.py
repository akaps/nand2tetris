import argparse
from pathlib import Path
import sys
from project_10.tokenizer import JackTokenizer
from project_10.compilation_engine import CompilationEngine
from symbol_table import SymbolTable
from vm_writer import VMWriter

JACK = '.jack'
VM = '.vm'

class JackCompiler:
    def __init__(self, file_name):
        self.file_name = file_name
        self.out_name = file_name.parent.joinpath(self.file_name.stem + VM)
        self.tokenizer = JackTokenizer(file_name)
        self.engine = CompilationEngine(self.tokenizer, self.out_name)
        self.table = SymbolTable()
        self.writer = VMWriter(self.out_name)

    def compile(self):
        print('compiling {file}'.format(file=self.file_name))
        #TODO the work with all the pieces
        self.writer.close()
        print('Successfully compiled {file} to {output}'.format(file=self.file_name, output=self.out_name))

def parse_args(args):
    usage = 'Compiles given .jack files for file/directory into Jack VM'
    parser = argparse.ArgumentParser(usage=usage)

    #positional arguments
    parser.add_argument('path',
        nargs=1,
        help='the path of the file(s) to analyze')

    return parser.parse_args(args)

def main(argv):
    args = parse_args(argv)
    path = Path(args.path[0])

    if path.is_file():
        compiler = JackCompiler(path)
        compiler.compile()
    else:
        for file_name in path.iterdir():
            if file_name.suffix == JACK:
                compiler = JackCompiler(file_name)
                compiler.compile()

if __name__ == '__main__':
    main(sys.argv[1:])
