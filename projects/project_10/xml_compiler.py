from xml.dom import minidom
import xml.etree.ElementTree as ET
import tokenizer
from compilation_engine import CompilationEngine

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
EXPRESSION_LIST = 'expressionList'
OPS = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
UNARY_OPS = ['-', '~']
KEYWORD_CONSTANTS = ['true', 'false', 'null', 'this']

#character constants
COMMA = ','
OPEN_BRACKET = '['
OPEN_PAREN = '('
CLOSE_PAREN = ')'
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
class XMLCompiler(CompilationEngine):
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

    def add_terminal(self, root, text):
        terminal = ET.SubElement(root, self.stream.token_type())
        terminal.text = ' {text} '.format(text=text)
        if self.stream.has_more_tokens():
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
        self.write()

    def compile_class_var_dec(self):
        '''
        compiles a static declaration or a field declaration.
        '''
        class_var_root = ET.SubElement(self.root, CLASS_VAR_DEC)
        self.add_terminal(class_var_root, self.stream.keyword())
        if self.stream.token_type() == tokenizer.KEYWORD:
            self.add_terminal(class_var_root, self.stream.keyword())
        else:
            self.add_terminal(class_var_root, self.stream.identifier())
        self.add_terminal(class_var_root, self.stream.identifier())

        while self.stream.symbol() == COMMA:
            self.add_terminal(class_var_root, self.stream.symbol())
            self.add_terminal(class_var_root, self.stream.identifier())

        self.add_terminal(class_var_root, self.stream.symbol())

    def compile_subroutine(self):
        '''
        compiles a complete method, function, or constructor.
        '''
        subroutine_dec = ET.SubElement(self.root, SUBROUTINE_DEC)
        self.add_terminal(subroutine_dec, self.stream.keyword())
        if self.stream.token_type() == tokenizer.KEYWORD:
            self.add_terminal(subroutine_dec, self.stream.keyword())
        else:
            self.add_terminal(subroutine_dec, self.stream.identifier())
        self.add_terminal(subroutine_dec, self.stream.identifier())

        self.add_terminal(subroutine_dec, self.stream.symbol())
        self.compile_parameter_list(subroutine_dec)
        self.add_terminal(subroutine_dec, self.stream.symbol())

        subroutine_body = ET.SubElement(subroutine_dec, SUBROUTINE_BODY)
        self.add_terminal(subroutine_body, self.stream.symbol())
        while self.stream.token_type() == tokenizer.KEYWORD and self.stream.keyword() == VAR:
            self.compile_var_dec(subroutine_body)
        self.compile_statements(subroutine_body)
        self.add_terminal(subroutine_body, self.stream.symbol())

    def compile_parameter_list(self, root):
        '''
        compiles a (possibly empty) parameter list, not including the enclosing “()”.
        '''
        parameter_list_root = ET.SubElement(root, PARAMETER_LIST)
        if self.stream.token_type() != tokenizer.SYMBOL:
            self.add_terminal(parameter_list_root, self.stream.keyword())
            self.add_terminal(parameter_list_root, self.stream.identifier())

        while self.stream.token_type() == tokenizer.SYMBOL and self.stream.symbol() == COMMA:
            self.add_terminal(parameter_list_root, self.stream.symbol())
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

        while self.stream.symbol() == COMMA:
            self.add_terminal(var_dec_root, self.stream.symbol())
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
        do_root = ET.SubElement(root, DO)
        self.add_terminal(do_root, self.stream.keyword())
        self.compile_subroutine_call(do_root)
        self.add_terminal(do_root, self.stream.symbol())

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
        while_root = ET.SubElement(root, WHILE)
        self.add_terminal(while_root, self.stream.keyword())
        self.add_terminal(while_root, self.stream.symbol())
        self.compile_expression(while_root)
        self.add_terminal(while_root, self.stream.symbol())
        self.add_terminal(while_root, self.stream.symbol())
        self.compile_statements(while_root)
        self.add_terminal(while_root, self.stream.symbol())

    def compile_return(self, root):
        '''
        compiles a return statement
        '''
        return_root = ET.SubElement(root, RETURN)
        self.add_terminal(return_root, self.stream.keyword())
        if self.stream.token_type() != tokenizer.SYMBOL:
            self.compile_expression(return_root)
        self.add_terminal(return_root, self.stream.symbol())

    def compile_if(self, root):
        '''
        compiles an if statement
        '''
        if_root = ET.SubElement(root, IF)
        self.add_terminal(if_root, self.stream.keyword())
        self.add_terminal(if_root, self.stream.symbol())
        self.compile_expression(if_root)
        self.add_terminal(if_root, self.stream.symbol())
        self.add_terminal(if_root, self.stream.symbol())
        self.compile_statements(if_root)
        self.add_terminal(if_root, self.stream.symbol())
        if self.stream.token_type() == tokenizer.KEYWORD and self.stream.keyword() == 'else':
            self.add_terminal(if_root, self.stream.keyword())
            self.add_terminal(if_root, self.stream.symbol())
            self.compile_statements(if_root)
            self.add_terminal(if_root, self.stream.symbol())

    def compile_expression(self, root):
        '''
        compiles an expression
        '''
        expression_root = ET.SubElement(root, EXPRESSION)
        self.compile_term(expression_root)
        while self.stream.token_type() == tokenizer.SYMBOL and self.stream.symbol() in OPS:
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
        elif token_type == tokenizer.KEYWORD and self.stream.keyword() in KEYWORD_CONSTANTS:
            self.add_terminal(term_root, self.stream.keyword())
        elif token_type == tokenizer.IDENTIFIER:
            if self.stream.peek() == OPEN_BRACKET:
                self.add_terminal(term_root, self.stream.identifier())
                self.add_terminal(term_root, self.stream.symbol())
                self.compile_expression(term_root)
                self.add_terminal(term_root, self.stream.symbol())
            elif self.stream.peek() == OPEN_PAREN or self.stream.peek() == PERIOD:
                self.compile_subroutine_call(term_root)
            else:
                self.add_terminal(term_root, self.stream.identifier())
        elif token_type == tokenizer.SYMBOL and self.stream.symbol() == OPEN_PAREN:
            self.add_terminal(term_root, self.stream.symbol())
            self.compile_expression(term_root)
            self.add_terminal(term_root, self.stream.symbol())
        elif token_type == tokenizer.SYMBOL and self.stream.symbol() in UNARY_OPS:
            self.add_terminal(term_root, self.stream.symbol())
            self.compile_term(term_root)
        else:
            assert False, 'unsupported token {token}'.format(token=self.stream.current_token)

    def compile_expression_list(self, root):
        '''
        compiles a (possibly empty) commaseparated list of expressions.
        '''
        expression_list_root = ET.SubElement(root, EXPRESSION_LIST)
        if self.stream.token_type() == tokenizer.SYMBOL and self.stream.symbol() == CLOSE_PAREN:
            return
        self.compile_expression(expression_list_root)
        while self.stream.symbol() == COMMA:
            self.add_terminal(expression_list_root, self.stream.symbol())
            self.compile_expression(expression_list_root)

    def compile_subroutine_call(self, root):
        self.add_terminal(root, self.stream.identifier())
        if self.stream.symbol() == PERIOD:
            self.add_terminal(root, self.stream.symbol())
            self.add_terminal(root, self.stream.identifier())
        self.add_terminal(root, self.stream.symbol())
        self.compile_expression_list(root)
        self.add_terminal(root, self.stream.symbol())

    def write(self):
        lines = self._write(self.root).split('\n')
        lines = lines[1:]
        file = open(self.out_file, 'w')
        file.write('\n'.join(lines))
        file.close()

    def _write(self, root):
        return minidom.parseString(ET.tostring(root)).toprettyxml()
