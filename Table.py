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
        
        self.cells = [ [ self.initCell( r, c )
                         for c in range( shape[ 1 ] ) ]
                       for r in range( shape[ 0 ] ) ]
        self.shape = list( shape )
    
    def initCell( self, row, column, **kwargs ):
        cell = self.makeCell( row, column, **kwargs )
        self.placeCell( cell, row, column )
        return cell
    
    def placeCell( self, cell, row, column ):
        cell.grid( row=row, column=column, sticky=tk.NSEW )

    def makeCell( self, row, column, **kwargs ):
        return tk.Entry( self, exportselection=0, **kwargs )

    def firstCell( self ):
        self.cells = [ [ self.makeCell( 0, 0 ) ] ]
        self.shape = [ 1, 1 ]

    def appendRow( self ):
        if self.cells is None:
            self.firstCell()
            return
        self.cells.append( [ self.makeCell( self.shape[ 0 ], c ) for c in range( self.shape[ 1 ] ) ] )
        self.shape[ 0 ] += 1
    
    def appendColumn( self ):
        if self.cells is None:
            self.firstCell()
            return
        for r, row in enumerate( self.cells ):
            row.append( self.makeCell( r, self.shape[ 1 ] ) )
        self.shape[ 1 ] += 1

class DfTable( Table ):
    'table initialized from and backed by a dataframe'
    def __init__( self, parent, df, **kwargs ):
        self.df = df.applymap( str )
        Table.__init__( self, parent, shape=list( df.shape ), **kwargs )
    
    def makeCell( self, row, column, **kwargs ):
        var = tk.StringVar( self )
        var.set( str( self.df.iloc[ row, column ] ) )
        def cb( *args, row=row, column=column, var=var ):
            self.df.iloc[ row, column ] = var.get()
        var.trace( 'w', cb )
        return Table.makeCell( self, row, column, textvariable=var, **kwargs )
    
    #def appendRow( self )
    #def appendColumn( self )