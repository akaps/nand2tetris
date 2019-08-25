def assert_unimplemented(name):
    assert False, 'calling superclass version of {name}'.format(name=name)

class CompilationEngine:

    def __init__(self, stream, out_file):
        assert_unimplemented('init')

    def compile_class(self):
        assert_unimplemented('compile_class')

    def compile_class_var_dec(self):
        assert_unimplemented('compile_class_var_dec')

    def compile_subroutine(self):
        assert_unimplemented('compile_subroutine')

    def compile_parameter_list(self):
        assert_unimplemented('compile_parameter_list')

    def compile_var_dec(self):
        assert_unimplemented('compile_var_dec')

    def compile_statements(self):
        assert_unimplemented('compile_statements')

    def compile_do(self):
        assert_unimplemented('compile_do')

    def compile_let(self):
        assert_unimplemented('compile_let')

    def compile_while(self):
        assert_unimplemented('compile_while')

    def compile_return(self):
        assert_unimplemented('compile_return')

    def compile_if(self):
        assert_unimplemented('compile_if')

    def compile_expression(self):
        assert_unimplemented('compile_expression')

    def compile_term(self):
        assert_unimplemented('compile_term')

    def compile_expression_list(self):
        assert_unimplemented('compile_expression_list')
