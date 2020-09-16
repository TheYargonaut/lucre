# implement basic spreadsheet-like display
# TODO:
# scrolling
# display a df (integrate. Root?)
# color highlighting
# scroll on whole frame? good enough for now, obviously good scaling opportunity

import tkinter as tk

class Table( tk.Frame ):
    def __init__( self, parent, shape=0, **kwargs ):
        tk.Frame.__init__( self, parent, **kwargs )

        if isinstance( shape, int ):
            shape = shape, shape

        if not ( shape[ 0 ] and shape[ 1 ] ):
            self.cells = None
            self.shape = [ 0, 0 ]
            return
        
        self.cells = [ [ self.makeCell( r, c )
                         for c in range( shape[ 1 ] ) ]
                       for r in range( shape[ 0 ] ) ]
        self.shape = list( shape )
    
    def makeCell( self, row, column ):
        cell = tk.Entry( self, exportselection=0 )
        cell.grid( row=row, column=column )
        return cell

    def firstCell( self ):
        self.cells = [ [ self.makeCell( 0, 0 ) ] ]
        self.shape = [ 1, 1 ]

    def appendRow( self ):
        if self.cells is None:
            self.firstCell()
            return
        self.cells.append( [ self.makeCell( self.shape[ 0 ], c ) for c in range( shape[ 1 ] ) ] )
        self.shape[ 0 ] += 1
    
    def appendColumn( self ):
        if self.cells is None:
            self.firstCell()
            return
        for r, row in enumerate( self.cells ):
            row.append( self.makeCell( r, self.shape[ 1 ] ) )
        self.shape[ 1 ] += 1

def tableFromDf( parent, df, header=False, index=False ):
    shape = list( df.shape )
    root = [ 0, 0 ]
    if header:
        shape[ 0 ] += 1
        root[ 0 ] = 1
    if index:
        shape[ 1 ] += 1
        root[ 1 ] += 1
    table = Table( parent, shape=shape )
    for rt, rd in zip( table.cells[ root[ 0 ]: ], df.iterrows() ):
        for ct, cd in zip( rt[ root[ 1 ]: ], rd[ 1 ] ):
            ct.insert( 0, str( cd ) )
    return table
