'''
The tokenizer removes all comments and white space from the input stream and breaks it into
Jack language tokens, as specified in the Jack grammar.
'''
class JackTokenizer:
    def __init__(self, file_name):
        '''
        Opens the input file/stream and gets ready to tokenize it
        '''
        assert False, 'unimplemented method {name}'.format(name=self.__init__.__name__)

    def has_more_tokens(self):
        '''
        do we have more tokens in the input?
        '''
        assert False, 'unimplemented method {name}'.format(name=self.has_more_tokens.__name__)

    def advance(self):
        '''
        gets the next token from the input and makes it the current token. This method
        should only be called if hasMoreTokens() is true. Initially there is no current token..
        '''
        assert False, 'unimplemented method {name}'.format(name=self.advance.__name__)

    def token_type(self):
        '''
        returns the type of the current token
        '''
        assert False, 'unimplemented method {name}'.format(name=self.token_type.__name__)

    def key_word(self):
        '''
        returns the keyword which is the current token.
        Should be called only when tokenType() is KEYWORD.
        '''
        assert False, 'unimplemented method {name}'.format(name=self.key_word.__name__)

    def symbol(self):
        '''
        returns the character which is the current token.
        Should be called only when tokenType() is SYMBOL.
        '''
        assert False, 'unimplemented method {name}'.format(name=self.symbol.__name__)

    def identifier(self):
        '''
        returns the identifier which is the current token.
        Should be called only when tokenType() is IDENTIFIER
        '''
        assert False, 'unimplemented method {name}'.format(name=self.identifier.__name__)

    def int_val(self):
        '''
        returns the integer value of the current token.
        Should be called only when tokenType() is INT_CONST
        '''
        assert False, 'unimplemented method {name}'.format(name=self.int_val.__name__)

    def string_val(self):
        '''
        returns the string value of the current token, without the double quotes.
        Should be called only when tokenType() is STRING_CONST.
        '''
        assert False, 'unimplemented method {name}'.format(name=self.string_val.__name__)
