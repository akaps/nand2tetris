import argparse
import sys
from pathlib import Path

from tokenizer import JackTokenizer
from compilation_engine import CompilationEngine

JACK = '.jack'
XML = '.xml'

def analyze(file_name):
    print('analyzing {file}'.format(file=file_name))
    out_name = file_name.parent.joinpath(file_name.stem + XML)
    tokenizer = JackTokenizer(file_name)
    engine = CompilationEngine(file_name, out_name)
    print('Successfully analyzed {file} to {output}'.format(files=file_name, output=out_name))

def parse_args(args):
    usage = 'Analyzes given .jack files for file/directory into Jack via .xml grammar'
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
        analyze(path)
    else:
        for file_name in path.iterdir():
            if file_name.suffix == JACK:
                analyze(file_name)

if __name__ == '__main__':
    main(sys.argv[1:])
