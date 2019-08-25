import argparse
import sys
from pathlib import Path

from tokenizer import JackTokenizer
from xml_compiler import XMLCompiler
from vm_compiler import VMCompiler

JACK = '.jack'
XML = '.xml'
VM = '.vm'

def process_file(file_name, is_analyze):
    tokenizer = JackTokenizer(file_name)
    print('processing {file}'.format(file=file_name))
    if is_analyze:
        out_name = file_name.parent.joinpath(file_name.stem + XML)
        engine = XMLCompiler(tokenizer, out_name)
        print('Successfully analyzed {file} to {output}'.format(file=file_name, output=out_name))
    else:
        out_name = file_name.parent.joinpath(file_name.stem + VM)
        engine = VMCompiler(tokenizer, out_name)
        print('Successfully compiled {file} to {output}'.format(file=file_name, output=out_name))
    engine.compile_class()

def parse_args(args):
    usage = 'Analyzes given .jack files for file/directory into Jack via .xml grammar'
    parser = argparse.ArgumentParser(usage=usage)

    #positional arguments
    parser.add_argument('path',
        nargs=1,
        help='the path of the file(s) to analyze')

    #optional arguments
    parser.add_argument('-a', '--analyze',
        dest='is_analyze',
        action='store_true')

    return parser.parse_args(args)

def main(argv):
    args = parse_args(argv)
    path = Path(args.path[0])
    is_analyze = args.is_analyze

    if path.is_file():
        process_file(path, is_analyze)
    else:
        for file_name in path.iterdir():
            if file_name.suffix == JACK:
                process_file(file_name, is_analyze)

if __name__ == '__main__':
    main(sys.argv[1:])
