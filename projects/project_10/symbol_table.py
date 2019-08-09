'''
A symbol table that associates names with information needed for Jack compilation: type, kind, and
running index. The symbol table has 2 nested scopes (class/subroutine).
'''
class SymbolTable:
    def __init__(self):
        '''
        Creates a new empty symbol table
        '''
        pass

    def start_subroutine(self):
        '''
        Starts a new subroutine scope (i.e. erases all names in the previous subroutine’s scope.)
        '''
        pass

    def define(self, name, type_name, kind):
        '''
        Defines a new identifier of a given name, type, and kind and assigns it a running
        index. STATIC and FIELD identifiers have a class scope, while ARG and VAR
        identifiers have a subroutine scope.
        '''
        pass

    def var_count(self, kind):
        '''
        Returns the number of variables of the given kind already defined in the current scope
        '''
        pass

    def kind_of(self, name):
        '''
        Returns the kind of the named identifier in the current scope.
        Returns None if the identifier is unknown in the current scope.
        '''
        pass

    def type_of(self, name):
        '''
        Returns the type of the named identifier in the current scope
        '''
        pass

    def index_of(self, name):
        '''
        Returns the index assigned to the named identifier
        '''
        pass
