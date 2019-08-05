from xml.dom import minidom
import xml.etree.ElementTree as ET
import tokenizer

#program structure constants
CLASS = 'class'
CLASS_VAR_DEC = 'classVarDec'
CLASS_VARS = ['static', 'field']
TYPES = ['int', 'char', 'boolean']
SUBROUTINE_DEC = 'subroutineDec'
SUBROUTINE_TYPES = ['constructor', 'function', 'method']
PARAMETER_LIST = 'parameterList'
SUBROUTINE_BODY = 'subroutineBody'
VAR_DEC = 'varDec'
VAR = 'var'
CLASS_NAME = 'className'
SUBROUTINE_NAME = 'subroutineName'
VAR_NAME = 'varName'

#statement constants
STATEMENTS = 'statements'
STATEMENT = 'statement'
LET = 'letStatement'
IF = 'ifStatement'
WHILE = 'whileStatement'
DO = 'doStatement'
RETURN = 'returnStatement'

#expression constants
EXPRESSION = 'expression'
TERM = 'term'
SUBROUTINE_CALL = 'subroutineCall'
EXPRESSION_LISt = 'expressionList'
OPS = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
UNARY_OPS = ['-', '~']
KEYWORD_CONSTANTS = ['true', 'false', 'null', 'this']

#character constants
COMMA = ','
OPEN_BRACKET = '['
OPEN_PAREN = '('
PERIOD = '.'

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
    def __init__(self, stream, out_file):
        '''
        creates a new compilation engine with the given input and output.
        The next method called must be compileClass().
        '''
        self.stream = stream
        self.out_file = out_file
        self.root = ET.Element('class')

        self.stream.advance()
        assert self.stream.keyword() == 'class'
        self.compile_class()

    def add_terminal(self, root, text):
        terminal = ET.SubElement(root, self.stream.token_type())
        terminal.text = text
        self.stream.advance()

    def compile_class(self):
        '''
        compiles a complete class
        '''
        self.add_terminal(self.root, self.stream.keyword())
        self.add_terminal(self.root, self.stream.identifier())
        self.add_terminal(self.root, self.stream.symbol())

        while self.stream.token_type() == tokenizer.KEYWORD and self.stream.keyword() in CLASS_VARS:
            self.compile_class_var_dec()

        while self.stream.token_type() == tokenizer.KEYWORD and self.stream.keyword() in SUBROUTINE_TYPES:
            self.compile_subroutine()

        self.add_terminal(self.root, self.stream.symbol())

    def compile_class_var_dec(self):
        '''
        compiles a static declaration or a field declaration.
        '''
        class_var_root = ET.SubElement(self.root, CLASS_VAR_DEC)
        self.add_terminal(class_var_root, self.stream.keyword())
        self.add_terminal(class_var_root, self.stream.keyword())
        self.add_terminal(class_var_root, self.stream.identifier())

        while self.stream.token_type() == tokenizer.KEYWORD and self.stream.symbol() == COMMA:
            self.add_terminal(class_var_root, self.stream.symbol())
            self.add_terminal(class_var_root, self.stream.identifier)

        self.add_terminal(class_var_root, self.stream.symbol())

    def compile_subroutine(self):
        '''
        compiles a complete method, function, or constructor.
        '''
        subroutine_root = ET.SubElement(self.root, SUBROUTINE_DEC)
        self.add_terminal(subroutine_root, self.stream.keyword())
        self.add_terminal(subroutine_root, self.stream.keyword())
        self.add_terminal(subroutine_root, self.stream.identifier())

        self.add_terminal(subroutine_root, self.stream.symbol())
        parameter_list = ET.SubElement(subroutine_root, PARAMETER_LIST)
        self.compile_parameter_list(parameter_list)
        self.add_terminal(subroutine_root, self.stream.symbol())

        subroutine_body = ET.SubElement(subroutine_root, SUBROUTINE_BODY)
        self.add_terminal(subroutine_body, self.stream.symbol())
        while self.stream.token_type() == tokenizer.KEYWORD and self.stream.keyword() == VAR:
            self.compile_var_dec(subroutine_body)
        self.compile_statements(subroutine_body)
        self.add_terminal(subroutine_root, self.stream.symbol())

    def compile_parameter_list(self, root):
        '''
        compiles a (possibly empty) parameter list, not including the enclosing “()”.
        '''
        parameter_list_root = ET.SubElement(root, PARAMETER_LIST)
        if self.stream.token_type() != tokenizer.SYMBOL:
            self.add_terminal(parameter_list_root, self.stream.keyword())
            self.add_terminal(parameter_list_root, self.stream.identifier())

        while self.stream.token_type() == tokenizer.SYMBOL and self.stream.symbol() == COMMA:
            self.add_terminal(parameter_list_root, self.stream.keyword())
            self.add_terminal(parameter_list_root, self.stream.identifier())

    def compile_var_dec(self, root):
        '''
        compiles a var declaration
        '''
        var_dec_root = ET.SubElement(root, VAR_DEC)
        self.add_terminal(var_dec_root, self.stream.keyword())
        if self.stream.token_type() == tokenizer.IDENTIFIER:
            self.add_terminal(var_dec_root, self.stream.identifier())
        else:
            self.add_terminal(var_dec_root, self.stream.keyword())
        self.add_terminal(var_dec_root, self.stream.identifier())
        self.add_terminal(var_dec_root, self.stream.symbol())

    def compile_statements(self, root):
        '''
        compiles a sequence of statements, not including the enclosing “{}”.
        '''
        statements_root = ET.SubElement(root, STATEMENTS)
        while self.stream.token_type() == tokenizer.KEYWORD:
            keyword = self.stream.keyword()
            if keyword == 'let':
                self.compile_let(statements_root)
            elif keyword == 'if':
                self.compile_if(statements_root)
            elif keyword == 'while':
                self.compile_while(statements_root)
            elif keyword == 'do':
                self.compile_do(statements_root)
            elif keyword == 'return':
                self.compile_return(statements_root)
            else:
                assert False, 'unsupported keyword {keyword}'.format(keyword=keyword)

    def compile_do(self, root):
        '''
        compiles a do statement
        '''
        assert False, 'unimplemented method {name}'.format(name=self.compile_do.__name__)

    def compile_let(self, root):
        '''
        compiles a let statement
        '''
        let_root = ET.SubElement(root, LET)
        self.add_terminal(let_root, self.stream.keyword())
        self.add_terminal(let_root, self.stream.identifier())
        if self.stream.token_type() == tokenizer.SYMBOL and self.stream.symbol() == OPEN_BRACKET:
            self.add_terminal(let_root, self.stream.symbol())
            self.compile_expression(let_root)
            self.add_terminal(let_root, self.stream.symbol())
        self.add_terminal(let_root, self.stream.symbol())
        self.compile_expression(let_root)
        self.add_terminal(let_root, self.stream.symbol())

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
        expression_root = ET.SubElement(root, EXPRESSION)
        self.compile_term(expression_root)
        while (self.stream.token_type() == tokenizer.SYMBOL and self.stream.symbol() in OPS):
            self.add_terminal(expression_root, self.stream.symbol())
            self.compile_term(expression_root)

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
        term_root = ET.SubElement(root, TERM)
        token_type = self.stream.token_type()
        if token_type == tokenizer.INT:
            self.add_terminal(term_root, self.stream.int_val())
        elif token_type == tokenizer.STRING:
            self.add_terminal(term_root, self.stream.string_val())
        elif token_type == KEYWORD_CONSTANTS:
            self.add_terminal(term_root, self.stream.keyword())
        elif token_type == tokenizer.IDENTIFIER:
            if self.stream.peek() == OPEN_BRACKET:
                self.add_terminal(term_root, self.stream.identifier())
                self.add_terminal(term_root, self.stream.symbol())
                self.compile_expression(term_root)
                self.add_terminal(term_root, self.stream.symbol())
            elif self.stream.peek() == OPEN_PAREN:
                self.compile_expression(term_root)
            elif self.stream.peek() == PERIOD:
                self.add_terminal(term_root, self.stream.identifier())
                if self.stream.symbol() == PERIOD:
                    self.add_terminal(term_root, self.stream.identifier())
                self.add_terminal(term_root, self.stream.symbol())
                self.compile_expression_list(term_root)
                self.add_terminal(term_root, self.stream.symbol())
            else:
                self.add_terminal(term_root, self.stream.identifier())

        elif token_type == tokenizer.SYMBOL and self.stream.symbol() in UNARY_OPS:
            self.add_terminal(term_root, self.stream.symbol())
        else:
            assert False, 'unsupported token {token}'.format(keyword=self.stream.current_token)

    def compile_expression_list(self, root):
        '''
        compiles a (possibly empty) commaseparated list of expressions.
        '''
        assert False, 'unimplemented method {name}'.format(name=self.compile_expression_list.__name__)

    def write(self):
        self._write(self.root)

    def _write(self, root):
        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent='    ')
        print(xmlstr)
