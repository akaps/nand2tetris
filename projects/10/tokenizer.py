from enum import Enum

SINGLE_COMMENT = '//'
MULTI_COMMENT = '/*'
END_COMMENT = '*/'
DOUBLE_QUOTES = '"'

KEYWORD_TYPE = 'keyword'
SYMBOL_TYPE = 'symbol'
IDENTIFIER_TYPE = 'identifier'
INT_CONST_TYPE = 'integerConstant'
STRING_CONST_TYPE = 'stringConstant'

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

SYMBOLS = [
    '{', '}',
    '(', ')',
    '[', ']',
    '.',
    ',',
    ';',
    '+',
    '-',
    '*',
    '/',
    '&',
    '|',
    '<',
    '>',
    '=',
    '~'
]

def _remove_multiline_comments(text, start_comment, end_comment):
    result = ''
    if start_comment in text:
        index = text.index(start_comment)
        result += text[:index]
        text = text[index+len(start_comment):]
        text = _remove_multiline_comments(text, start_comment, end_comment)
        index = text.index(end_comment)
        result += text[index + len(end_comment):]
    else:
        result = text
    return result

def remove_multiline_comments(lines):
    text = '\n'.join(lines)
    while MULTI_COMMENT in text:
        text = _remove_multiline_comments(text, MULTI_COMMENT, END_COMMENT)
    return text.strip()

def tokenize(lines):
    print(lines)
    return lines.split()

def preprocess_file(file_name):
    file = open(file_name, 'r')
    result = []
    for line in file.readlines():
        line = line.strip()
        if SINGLE_COMMENT in line:
            comment_index = line.index(SINGLE_COMMENT)
            line = line[:comment_index].strip()
        if line:
            result.append(line)
    file.close()
    lines = remove_multiline_comments(result)
    return tokenize(lines)

'''
The tokenizer removes all comments and white space from the input stream and breaks it into
Jack language tokens, as specified in the Jack grammar.
'''
class JackTokenizer:
    def __init__(self, file_name):
        '''
        Opens the input file/stream and gets ready to tokenize it
        '''
        self.tokens = preprocess_file(file_name)
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

    def token_type(self):
        '''
        returns the type of the current token
        '''
        if self.current_token in KEYWORDS:
            return KEYWORD_TYPE
        elif self.current_token in SYMBOLS:
            return SYMBOL_TYPE
        elif self.current_token.isdigit():
            return INT_CONST_TYPE
        elif DOUBLE_QUOTES in self.current_token:
            return STRING_CONST_TYPE
        return IDENTIFIER_TYPE

    def check_type_match(self, token_type):
        assert self.token_type() == token_type, 'invalid call to "{token_type}", token "{token}" is {type}'.format(
            token_type=token_type,
            type=self.token_type(),
            token=self.current_token)

    def keyword(self):
        '''
        returns the keyword which is the current token.
        Should be called only when tokenType() is KEYWORD.
        '''
        self.check_type_match(KEYWORD_TYPE)
        return self.current_token

    def symbol(self):
        '''
        returns the character which is the current token.
        Should be called only when tokenType() is SYMBOL.
        '''
        self.check_type_match(SYMBOL_TYPE)
        return self.current_token

    def identifier(self):
        '''
        returns the identifier which is the current token.
        Should be called only when tokenType() is IDENTIFIER
        '''
        self.check_type_match(IDENTIFIER_TYPE)
        return self.current_token

    def int_val(self):
        '''
        returns the integer value of the current token.
        Should be called only when tokenType() is INT_CONST
        '''
        self.check_type_match(INT_CONST_TYPE)
        assert False, 'unimplemented method {name}'.format(name=self.int_val.__name__)

    def string_val(self):
        '''
        returns the string value of the current token, without the double quotes.
        Should be called only when tokenType() is STRING_CONST.
        '''
        self.check_type_match(STRING_CONST_TYPE)
        assert False, 'unimplemented method {name}'.format(name=self.string_val.__name__)
