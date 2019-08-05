from xml.dom import minidom
import xml.etree.ElementTree as ET

CLASS_VAR_DEC = 'classVarDec'
CLASS_VARS = ['static', 'field']

SUBROUTINE_DEC = 'subroutineDec'
SUBROUTINES = ['constructor', 'function', 'method']

SUBROUTINE_BODY = 'subroutineBody'
PARAMETER_LIST = 'parameterList'

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
    def __init__(self, tokenizer, out_file):
        '''
        creates a new compilation engine with the given input and output.
        The next method called must be compileClass().
        '''
        self.tokenizer = tokenizer
        self.out_file = out_file
        self.root = ET.Element('class')

        self.tokenizer.advance()
        assert self.tokenizer.keyword() == 'class'
        self.compile_class()

    def add_terminal(self, root, text):
        terminal = ET.SubElement(root, self.tokenizer.token_type())
        terminal.text = text
        self.tokenizer.advance()

    def compile_class(self):
        '''
        compiles a complete class
        '''
        self.add_terminal(self.root, self.tokenizer.keyword())
        self.add_terminal(self.root, self.tokenizer.identifier())
        self.add_terminal(self.root, self.tokenizer.symbol())

        while self.tokenizer.token_type() == 'keyword' and self.tokenizer.keyword() in CLASS_VARS:
            self.compile_class_var_dec()

        self.write()

        while self.tokenizer.token_type() == 'keyword' and self.tokenizer.keyword() in SUBROUTINES:
            self.compile_subroutine()

        self.add_terminal(self.root, self.tokenizer.symbol())

    def compile_class_var_dec(self):
        '''
        compiles a static declaration or a field declaration.
        '''
        class_var_root = ET.SubElement(self.root, CLASS_VAR_DEC)
        self.add_terminal(class_var_root, self.tokenizer.keyword())
        self.add_terminal(class_var_root, self.tokenizer.keyword())
        self.add_terminal(class_var_root, self.tokenizer.identifier())

        while self.tokenizer.token_type() == 'symbol' and self.tokenizer.symbol() == ',':
            self.add_terminal(class_var_root, self.tokenizer.symbol())
            self.add_terminal(class_var_root, self.tokenizer.identifier)

        self.add_terminal(class_var_root, self.tokenizer.symbol())

    def compile_subroutine(self):
        '''
        compiles a complete method, function, or constructor.
        '''
        subroutine_root = ET.SubElement(self.root, SUBROUTINE_DEC)
        self.add_terminal(subroutine_root, self.tokenizer.keyword())
        self.add_terminal(subroutine_root, self.tokenizer.keyword())
        self.add_terminal(subroutine_root, self.tokenizer.identifier())

        self.add_terminal(subroutine_root, self.tokenizer.symbol())
        parameter_list = ET.SubElement(subroutine_root, PARAMETER_LIST)
        self.compile_parameter_list(parameter_list)
        self.add_terminal(subroutine_root, self.tokenizer.symbol())

        subroutine_body = ET.SubElement(subroutine_root, SUBROUTINE_BODY)
        self.add_terminal(subroutine_body, self.tokenizer.symbol())
        while self.tokenizer.token_type() == 'keyword':
            if self.tokenizer.keyword() == 'identifier':
                self.compile_var_dec(subroutine_body)
            else:
                self.compile_statements(subroutine_body)
        self.add_terminal(subroutine_root, self.tokenizer.symbol())

    def compile_parameter_list(self, root):
        '''
        compiles a (possibly empty) parameter list, not including the enclosing “()”.
        '''
        if self.tokenizer.token_type() != 'symbol':
            self.add_terminal(root, self.tokenizer.keyword())
            self.add_terminal(root, self.tokenizer.identifier())

        while self.tokenizer.token_type() == 'symbol' and self.tokenizer.symbol() == ',':
            self.add_terminal(root, self.tokenizer.keyword())
            self.add_terminal(root, self.tokenizer.identifier())

    def compile_var_dec(self, root):
        '''
        compiles a var declaration
        '''
        assert False, 'unimplemented method {name}'.format(name=self.compile_var_dec.__name__)

    def compile_statements(self, root):
        '''
        compiles a sequence of statements, not including the enclosing “{}”.
        '''
        if self.tokenizer.keyword() == 'let':
            self.compile_let(root)
        if self.tokenizer.keyword() == 'if':
            self.compile_if(root)
        if self.tokenizer.keyword() == 'while':
            self.compile_while(root)
        if self.tokenizer.keyword() == 'do':
            self.compile_do(root)
        if self.tokenizer.keyword() == 'return':
            self.compile_return(root)
        assert False, 'unimplemented method {name}'.format(name=self.compile_statements.__name__)

    def compile_do(self, root):
        '''
        compiles a do statement
        '''
        assert False, 'unimplemented method {name}'.format(name=self.compile_do.__name__)

    def compile_let(self, root):
        '''
        compiles a let statement
        '''
        assert False, 'unimplemented method {name}'.format(name=self.compile_let.__name__)

    def compile_while(self, root):
        '''
        compiles a while statement
        '''
        assert False, 'unimplemented method {name}'.format(name=self.compile_while.__name__)

    def compile_return(self, root):
        '''
        compiles a return statement
        '''
        assert False, 'unimplemented method {name}'.format(name=self.compile_return.__name__)

    def compile_if(self, root):
        '''
        compiles an if statement
        '''
        assert False, 'unimplemented method {name}'.format(name=self.compile_if.__name__)

    def compile_expression(self, root):
        '''
        compiles an expression
        '''
        assert False, 'unimplemented method {name}'.format(name=self.compile_expression.__name__)

    def compile_term(self, root):
        '''
        compiles a term. This method is faced with a slight difficulty when trying to
        decide between some of the alternative rules. Specifically, if the current token
        is an identifier, it must still distinguish between a variable, an array entry, and
        a subroutine call. The distinction can be made by looking ahead one extra token.
        A single look-ahead token, which may be one of “[“, “(“, “.”, suffices to
        distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        '''
        assert False, 'unimplemented method {name}'.format(name=self.compile_term.__name__)

    def compile_expression_list(self, root):
        '''
        compiles a (possibly empty) commaseparated list of expressions.
        '''
        assert False, 'unimplemented method {name}'.format(name=self.compile_expression_list.__name__)

    def write(self):
        xmlstr = minidom.parseString(ET.tostring(self.root)).toprettyxml(indent='    ')
        print(xmlstr)
