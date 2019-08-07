import collections

def UNFINISHED(method):
    assert False, 'Unfinished method {name}'.format(name=method.__name__)

CLASS = 'class'
SUBROUTINE = 'subroutine'

STATIC = 'static'
FIELD = 'field'
ARG = 'arg'
VAR = 'var'

SCOPE = {
    STATIC : CLASS,
    FIELD : CLASS,
    ARG : SUBROUTINE,
    VAR : SUBROUTINE
}

NAME = 'name'
TYPE = 'type'
KIND = 'kind'
INDEX = 'index'

Symbol = collections.namedtuple('Symbol', [NAME, TYPE, KIND, INDEX])

'''
A symbol table that associates names with information needed for Jack compilation: type, kind, and
running index. The symbol table has 2 nested scopes (class/subroutine).
'''
class SymbolTable:
    def __init__(self):
        '''
        Creates a new empty symbol table
        '''
        self.table = {}
        self.table[CLASS] = {}
        self.table[SUBROUTINE] = {}

    def start_subroutine(self):
        '''
        Starts a new subroutine scope (i.e. erases all names in the previous subroutine’s scope.)
        '''
        UNFINISHED(self.start_subroutine)

    def define(self, name, identifier_type, kind):
        '''
        Defines a new identifier of a given name, type, and kind and assigns it a running
        index. STATIC and FIELD identifiers have a class scope, while ARG and VAR
        identifiers have a subroutine scope.
        '''
        UNFINISHED(self.define)

    def var_count(self, kind):
        '''
        Returns the number of variables of the given kind already defined in the current scope.
        '''
        UNFINISHED(self.var_count)

    def kind_of(self, name):
        '''
        Returns the kind of the named identifier in the current scope. Returns NONE if the
        identifier is unknown in the current scope
        '''
        UNFINISHED(self.kind_of)

    def type_of(self, name):
        '''
        Returns the type of the named identifier in the current scope.
        '''
        UNFINISHED(self.type_of)

    def index_of(self, name):
        '''
        Returns the index assigned to named identifier.
        '''
        UNFINISHED(self.index_of)
