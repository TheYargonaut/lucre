import os, yaml

internalFmt = [ 'date', 'delta', 'memo' ]
defaultFile = os.path.join( '.', 'userdata', 'formats.yaml' )

class FormatMan( object ):
    def __init__( self, formats={} ):
        self.formats = formats
    
    def load( self, filename=defaultFile ):
        try:
            with open( filename, 'r' ) as f:
                self.formats.update( yaml.load( f, Loader=yaml.FullLoader ) )
            return True
        except FileNotFoundError:
            return False

    def save( self, filename=defaultFile ):
        with open( filename, 'w' ) as f:
            yaml.dump( self.formats, f )