import collections

'''
A symbol table that associates names with information needed for Jack compilation: type, kind, and
running index. The symbol table has 2 nested scopes (class/subroutine).
'''

STATIC = 'static'
FIELD = 'field'
ARGUMENT = 'argument'
VAR = 'var'

Symbol = collections.namedtuple('Symbol', ['name', 'type', 'kind', 'index'])

class SymbolTable:
    def __init__(self):
        '''
        Creates a new empty symbol table
        '''
        self.class_table = {}
        self.static_num = 0
        self.field_num = 0
        self.start_subroutine()

    def start_subroutine(self):
        '''
        Starts a new subroutine scope (i.e. erases all names in the previous subroutine’s scope.)
        '''
        self.subroutine_table = {}
        self.argument_num = 0
        self.var_num = 0

    def define(self, name, type_name, kind):
        '''
        Defines a new identifier of a given name, type, and kind and assigns it a running
        index. STATIC and FIELD identifiers have a class scope, while ARG and VAR
        identifiers have a subroutine scope.
        '''
        index = 0
        if kind in [STATIC, FIELD]:
            if kind == STATIC:
                index = self.static_num
                self.static_num += 1
            else:
                index = self.field_num
                self.field_num += 1
            self.class_table[name] = Symbol(name, type_name, kind, index)
        else:
            if kind == ARGUMENT:
                index = self.argument_num
                self.argument_num += 1
            else:
                index = self.var_num
                self.var_num += 1
            self.subroutine_table[name] = Symbol(name, type_name, kind, index)

    def var_count(self, kind):
        '''
        Returns the number of variables of the given kind already defined in the current scope
        '''
        counts = {
            STATIC : self.static_num,
            FIELD : self.field_num,
            ARGUMENT : self.argument_num,
            VAR : self.var_num
        }
        return counts[kind]

    def kind_of(self, name):
        '''
        Returns the kind of the named identifier in the current scope.
        Returns None if the identifier is unknown in the current scope.
        '''
        if name in self.class_table:
            return self.class_table[name].kind
        elif name in self.subroutine_table:
            return self.subroutine_table[name].kind
        return None

    def type_of(self, name):
        '''
        Returns the type of the named identifier in the current scope
        '''
        if name in self.class_table:
            return self.class_table[name].type
        return self.subroutine_table[name].type

    def index_of(self, name):
        '''
        Returns the index assigned to the named identifier
        '''
        if name in self.class_table:
            return self.class_table[name].index
        return self.subroutine_table[name].index
