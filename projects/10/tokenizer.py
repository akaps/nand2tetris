import collections
import re


COMMENT = 'comment'
KEYWORD = 'keyword'
SYMBOL = 'symbol'
IDENTIFIER = 'identifier'
INT = 'integerConstant'
STRING = 'stringConstant'

KEYWORDS = [
    'class',
    'constructor',
    'function',
    'method',
    'field',
    'static',
    'var',
    'int',
    'char',
    'boolean',
    'void',
    'true',
    'false',
    'null',
    'this',
    'let',
    'do',
    'if',
    'else',
    'while',
    'return'
]

Token = collections.namedtuple('Token', ['type', 'value'])

def tokenize(file_name):
    MISMATCH = 'mismatch'
    SKIP = 'skip'

    file = open(file_name, 'r')
    input = '\n'.join(file.readlines())
    file.close()

    TOKEN_SPECIFICATION = [
        (COMMENT,       r'(\/\/.*)|(\/\*(.|[\r\n])*?\*\/)'),
        (INT,           r'\d+'),
        (IDENTIFIER,    r'[_a-zA-Z][_a-zA-Z0-9]*'),
        (STRING,        r'".+"'),
        (SKIP,          r'[ \t\n]'),
        (SYMBOL,        r'[\{\}\(\)\[\]\.\+\*\-,;/&\|<>=~;]'),
        (MISMATCH,      r'.')
    ]
    token_regex = r'|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)
    result = []
    for match in re.finditer(token_regex, input):
        kind = match.lastgroup
        value = match.group()
        if kind == INT:
            value = int(value)
        elif kind == IDENTIFIER and value in KEYWORDS:
            kind = KEYWORD
        elif kind == SKIP or kind == COMMENT:
            continue
        elif kind == STRING:
            value = value[1:-1]
        elif kind == MISMATCH:
            assert False, 'unexpected value {value}'.format(value=value)
        result.append(Token(kind, value))
    return result

'''
The tokenizer removes all comments and white space from the input stream and breaks it into
Jack language tokens, as specified in the Jack grammar.
'''
class JackTokenizer:
    def __init__(self, file_name):
        '''
        Opens the input file/stream and gets ready to tokenize it
        '''
        self.tokens = tokenize(file_name)
        self.current_token = None
        self.next_token = 0

    def has_more_tokens(self):
        '''
        do we have more tokens in the input?
        '''
        return self.next_token < len(self.tokens)

    def advance(self):
        '''
        gets the next token from the input and makes it the current token. This method
        should only be called if hasMoreTokens() is true. Initially there is no current token..
        '''
        self.current_token = self.tokens[self.next_token]
        self.next_token += 1

    def peek(self):
        '''
        looks ahead at the next token.
        Useful for disambiguating an identifier term from variable, array entry, or subroutine call
        '''
        return self.tokens[self.next_token][1]

    def token_type(self):
        '''
        returns the type of the current token
        '''
        return self.current_token[0]

    def check_type_match(self, token_type):
        assert self.token_type() == token_type, 'invalid call to "{token_type}", token is "{token}"'.format(
            token_type=token_type,
            token=self.current_token)

    def keyword(self):
        '''
        returns the keyword which is the current token.
        Should be called only when tokenType() is KEYWORD.
        '''
        self.check_type_match(KEYWORD)
        return self.current_token[1]

    def symbol(self):
        '''
        returns the character which is the current token.
        Should be called only when tokenType() is SYMBOL.
        '''
        self.check_type_match(SYMBOL)
        return self.current_token[1]

    def identifier(self):
        '''
        returns the identifier which is the current token.
        Should be called only when tokenType() is IDENTIFIER
        '''
        self.check_type_match(IDENTIFIER)
        return self.current_token[1]

    def int_val(self):
        '''
        returns the integer value of the current token.
        Should be called only when tokenType() is INT_CONST
        '''
        self.check_type_match(INT)
        return self.current_token[1]

    def string_val(self):
        '''
        returns the string value of the current token, without the double quotes.
        Should be called only when tokenType() is STRING_CONST.
        '''
        self.check_type_match(STRING)
        return self.current_token[1]
