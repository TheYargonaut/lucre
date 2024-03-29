import tkinter as tk
from tkinter import ttk

class ListView( ttk.Frame ):
    def __init__( self, parent, back=[], addButton=None, cb=lambda idx:None, **kwargs ):
        'pass a string as addButton to make button and label with that string'
        ttk.Frame.__init__( self, parent, **kwargs)
        self.columnconfigure( 0, weight=1 )
        self.back = back
        self.addButton = addButton
        if not addButton is None:
            self.addButton = ttk.Button( self, text=str( addButton ), command=self.appendCell )
            self.addButton.pack( side=tk.BOTTOM, fill=tk.X, expand=True )
        self.cb = cb
        if isinstance( back, dict ):
            self.cells = [ self.initCell( k ) for k in self.back.keys() ]
        else:
            self.cells = [ self.initCell( i ) for i, _ in enumerate( self.back )  ]
    
    def appendCell( self ):
        self.back.append( '' )
        idx = len( self.back ) - 1
        self.cells.append( self.initCell( idx ) )
        self.cb( idx, '' )
    
    def initCell( self, label ):
        cell = self.makeCell( label )
        self.placeCell( cell, label )
        return cell

    def makeCell( self, label, **kwargs ):
        var = tk.StringVar( self )
        var.set( str( self.back[ label ] ) )
        def cb( *args, label=label, var=var ):
            self.cb( label, var.get() )
        var.trace( 'w', cb )
        return ttk.Entry( self, textvariable=var, **kwargs )

    def placeCell( self, cell, label ):
        cell.pack( side=tk.TOP, fill=tk.X, expand=True )