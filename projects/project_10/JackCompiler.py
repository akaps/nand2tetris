import argparse
import sys
from pathlib import Path

from tokenizer import JackTokenizer
from compilation_engine import CompilationEngine

JACK = '.jack'
XML = '.xml'
VM = '.vm'

def compile(file_name, analyze):
    vm_name = file_name.parent.joinpath(file_name.stem + VM)
    xml_name = file_name.parent.joinpath(file_name.stem + XML) if analyze else None

    tokenizer = JackTokenizer(file_name)
    engine = CompilationEngine(tokenizer, vm_name, xml_name)
    print('compiling {file}'.format(file=file_name))
    engine.compile_class()
    engine.write()
    print('Successfully compiled {file} to {output}'.format(file=file_name, output=vm_name))

def parse_args(args):
    usage = 'Analyzes given .jack files for file/directory into Jack via .xml grammar'
    parser = argparse.ArgumentParser(usage=usage)

    #positional arguments
    parser.add_argument('path',
        nargs=1,
        help='the path of the file(s) to analyze')

    #optional arguments
    parser.add_argument('-a', '--analyze',
        action='store_true',
        help='analyzes the file(s) and reports the structure as XML as well')

    return parser.parse_args(args)

def main(argv):
    args = parse_args(argv)
    path = Path(args.path[0])

    if path.is_file():
        compile(path, args.analyze)
    else:
        for file_name in path.iterdir():
            if file_name.suffix == JACK:
                compile(file_name, args.analyze)

if __name__ == '__main__':
    main(sys.argv[1:])
