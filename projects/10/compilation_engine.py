'''
This module effects the actual compilation into XML form. It gets its input from a JackTokenizer and
writes its parsed XML structure into an output file/stream. This is done by a series of compilexxx()
methods, where xxx is a corresponding syntactic element of the Jack grammar. The contract between these
methods is that each compilexxx() method should read the syntactic construct xxx from the input,
advance() the tokenizer exactly beyond xxx, and output the XML parsing of xxx. Thus,
compilexxx()may only be called if indeed xxx is the next syntactic element of the input.
In the next chapter, this module will be modified to output the compiled code rather than XML.
'''
class CompilationEngine:
    def __init__(self, in_file, out_file):
        '''
        creates a new compilation engine with the given input and output.
        The next method called must be compileClass().
        '''
        assert False, 'unimplemented method {name}'.format(name=__name__)

    def compile_class(self):
        '''
        compiles a complete class
        '''

    def compile_class_var_dec(self):
        '''
        compiles a static declaration or a field declaration.
        '''
        assert False, 'unimplemented method {name}'.format(name=__name__)

    def compile_subroutine(self):
        '''
        compiles a complete method, function, or constructor.
        '''
        assert False, 'unimplemented method {name}'.format(name=__name__)

    def compile_parameter_list(self):
        '''
        compiles a (possibly empty) parameter list, not including the enclosing “()”.
        '''
        assert False, 'unimplemented method {name}'.format(name=__name__)

    def compile_var_dec(self):
        '''
        compiles a var declaration
        '''
        assert False, 'unimplemented method {name}'.format(name=__name__)

    def compile_statements(self):
        '''
        compiles a sequence of statements, not including the enclosing “{}”.
        '''
        assert False, 'unimplemented method {name}'.format(name=__name__)

    def compile_do(self):
        '''
        compiles a do statement
        '''
        assert False, 'unimplemented method {name}'.format(name=__name__)

    def compile_let(self):
        '''
        compiles a let statement
        '''
        assert False, 'unimplemented method {name}'.format(name=__name__)

    def compile_while(self):
        '''
        compiles a while statement
        '''
        assert False, 'unimplemented method {name}'.format(name=__name__)

    def compile_return(self):
        '''
        compiles a return statement
        '''
        assert False, 'unimplemented method {name}'.format(name=__name__)

    def compile_if(self):
        '''
        compiles an if statement
        '''
        assert False, 'unimplemented method {name}'.format(name=__name__)

    def compile_expression(self):
        '''
        compiles an expression
        '''
        assert False, 'unimplemented method {name}'.format(name=__name__)

    def compile_term(self):
        '''
        compiles a term. This method is faced with a slight difficulty when trying to
        decide between some of the alternative rules. Specifically, if the current token
        is an identifier, it must still distinguish between a variable, an array entry, and
        a subroutine call. The distinction can be made by looking ahead one extra token.
        A single look-ahead token, which may be one of “[“, “(“, “.”, suffices to
        distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        '''
        assert False, 'unimplemented method {name}'.format(name=__name__)

    def compile_expression_list(self):
        '''
        compiles a (possibly empty) commaseparated list of expressions.
        '''
        assert False, 'unimplemented method {name}'.format(name=__name__)
