from Ledger import internalFmt
from Scrollable import Scrollable
from Table import DfTable, Table
from tkinter import ttk
import pandas as pd
import tkinter as tk

defaultColumn = 'ignore'
prevLens = [ 10, 25, 100 ]

class HeadingFmtTable( DfTable ):
    def __init__( self, parent, df, headingCb, **kwargs ):
        self.df = df.applymap( str )
        self.headingCb = headingCb
        shape = list( df.shape )
        shape[ 0 ] += 1
        Table.__init__( self, parent, shape=shape, **kwargs )
    
    def makeHeader( self, column, **kwargs ):
        def cb( value, pos=column ):
            self.headingCb( value, pos )
        return ttk.OptionMenu( self, tk.StringVar( self ), defaultColumn, defaultColumn, *internalFmt, command=cb )
    
    def makeCell( self, row, column, **kwargs ):
        if not row:
            return self.makeHeader( column, **kwargs )
        return DfTable.makeCell( self, row - 1, column, **kwargs )

class ImportLedgerWindow( tk.Toplevel ):
    def __init__( self, master, ledger, format, df, psize, *args, **kwargs ):
        tk.Toplevel.__init__( self, master, *args, **kwargs )
        self.ledger = ledger
        self.df = df
        self.psize = psize
        self.table = None
        self.headerFmt = [ defaultColumn ] * df.shape[ 1 ]
        self.build()
    
    def finalize( self ):
        fmt = [ name if name in internalFmt else str( i )
                for i, name in enumerate( self.headerFmt ) ]
        self.df.columns = fmt
        self.ledger.add( self.df )
        self.destroy()
    
    def updateFmt( self, value, pos ):
        if value in internalFmt:
            for f, h in zip( self.headerFmt, self.table.headVar ):
                if f == value:
                    h.set( 'ignore' )
        self.headerFmt[ pos ] = value
        if all( self.headerFmt.count( name ) == 1 for name in internalFmt ):
            self.confirm.configure( state=tk.NORMAL )
        else:
            self.confirm.configure( state=tk.DISABLED )
    
    def resizePreview( self, size ):
        if self.table is not None:
            self.table.destroy()
            self.table = None
        self.table = HeadingFmtTable( self.scroll, self.df.head( int( size ) ), self.updateFmt )
        self.table.pack( side=tk.TOP, fill=tk.BOTH, expand=True )

    def build( self ):
        button = ttk.Frame( self )
        button.pack( side=tk.BOTTOM, fill=tk.X )
        cancel = ttk.Button( button, text="Cancel", command=self.destroy )
        cancel.pack( side=tk.RIGHT )
        self.confirm = ttk.Button( button, text="Confirm", command=self.finalize, state=tk.DISABLED )
        self.confirm.pack( side=tk.RIGHT )
        prevLenMenu = ttk.OptionMenu( button, tk.StringVar( button ), str( self.psize ), *( [ str( p ) for p in prevLens if p < self.df.shape[ 0 ] ] + [ self.df.shape[ 0 ] ] ), command=self.resizePreview )
        prevLenMenu.pack( side=tk.LEFT )

        self.scroll = Scrollable( self, horizontal=True, vertical=True )
        self.scroll.pack( side=tk.TOP, fill=tk.BOTH, expand=True )
        self.resizePreview( str( self.psize ) )

def importLedgerCb( master, ledger, format, psize ):
    def cb( master=master, ledger=ledger, format=format, psize=psize ):
        f = tk.filedialog.askopenfilename()
        if not f:
            return
        df = pd.read_csv( f, index_col=None, header=None )
        window = ImportLedgerWindow( master, ledger, format, df, psize )
        master.wait_window( window )
    return cb