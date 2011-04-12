class VarNestedException( Exception ):
    """A variable grouping was nested.
    Not currently allowed."""
    position = 0
    def __init__( self, position ):
        self.position = position

    def __str__( self ):
        return repr(self.position)

class VarMultipleException( Exception ):
    """Another variable grouping in the current equation.
    Not currently allowed."""
    position = 0
    def __init__( self, position ):
        self.position = position

    def __str__( self ):
        return repr(self.position)


