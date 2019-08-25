def assert_unimplemented(name):
    assert False, 'calling superclass version of {name}'.format(name=name)

'''
This module provides an abstract solution for compilation. It gets its input from a JackTokenizer and
writes its output to a specified file file/stream. This is done by a series of compilexxx()
methods, where xxx is a corresponding syntactic element of the Jack grammar. The contract between these
methods is that each compilexxx() method should read the syntactic construct xxx from the input,
advance() the tokenizer exactly beyond xxx, and write the corresponding output. Thus,
compilexxx()may only be called if indeed xxx is the next syntactic element of the input.
'''
class CompilationEngine:

    def __init__(self, stream, out_file):
        '''
        creates a new compilation engine with the given input and output.
        The next method called must be compileClass().
        '''
        assert_unimplemented('init')

    def compile_class(self):
        '''
        compiles a complete class
        '''
        assert_unimplemented('compile_class')

    def compile_class_var_dec(self):
        '''
        compiles a static declaration or a field declaration.
        '''
        assert_unimplemented('compile_class_var_dec')

    def compile_subroutine(self):
        '''
        compiles a complete method, function, or constructor.
        '''
        assert_unimplemented('compile_subroutine')

    def compile_parameter_list(self):
        '''
        compiles a (possibly empty) parameter list, not including the enclosing “()”.
        '''
        assert_unimplemented('compile_parameter_list')

    def compile_var_dec(self):
        '''
        compiles a var declaration
        '''
        assert_unimplemented('compile_var_dec')

    def compile_statements(self):
        '''
        compiles a sequence of statements, not including the enclosing “{}”.
        '''
        assert_unimplemented('compile_statements')

    def compile_do(self):
        '''
        compiles a do statement
        '''
        assert_unimplemented('compile_do')

    def compile_let(self):
        '''
        compiles a let statement
        '''
        assert_unimplemented('compile_let')

    def compile_while(self):
        '''
        compiles a while statement
        '''
        assert_unimplemented('compile_while')

    def compile_return(self):
        '''
        compiles a return statement
        '''
        assert_unimplemented('compile_return')

    def compile_if(self):
        '''
        compiles an if statement
        '''
        assert_unimplemented('compile_if')

    def compile_expression(self):
        '''
        compiles an expression
        '''
        assert_unimplemented('compile_expression')

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
        assert_unimplemented('compile_term')

    def compile_expression_list(self):
        '''
        compiles a (possibly empty) commaseparated list of expressions.
        '''
        assert_unimplemented('compile_expression_list')
