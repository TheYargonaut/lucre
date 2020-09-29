import tkinter as tk

class ListView( tk.Frame ):
    def __init__( self, parent, back=[], addButton=None, cb=lambda idx:None, **kwargs ):
        'pass a string as addButton to make button and label with that string'
        tk.Frame.__init__( self, parent, **kwargs)
        self.back = back
        self.addButton = addButton
        if not addButton is None:
            self.addButton = tk.Button( self, text=str( addButton ), command=self.appendCell )
            # can I use pack to make button movement automatic?
            self.addButton.pack( side=tk.BOTTOM, fill=tk.X, expand=True )
        self.cb = cb
        self.cells = [ self.initCell( i ) for i in range( len( self.back ) ) ]
    
    def appendCell( self ):
        self.back.append( '' )
        self.cells.append( self.initCell( len( self.back ) - 1 ) )
    
    def initCell( self, index ):
        cell = self.makeCell( index )
        self.placeCell( cell, index )
        return cell

    def makeCell( self, index, **kwargs ):
        var = tk.StringVar( self )
        var.set( str( self.back[ index ] ) )
        def cb( *args, index=index, var=var ):
            self.back[ index ] = var.get()
            self.cb( index )
        var.trace( 'w', cb )
        return tk.Entry( self, textvariable=var, **kwargs )

    def placeCell( self, cell, index ):
        cell.pack( side=tk.TOP, fill=tk.X, expand=True )