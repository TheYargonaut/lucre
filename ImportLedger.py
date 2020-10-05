# dialog window to import ledger
import tkinter as tk
import pandas as pd
from Scrollable import Scrollable
from Table import DfTable, Table
from Ledger import internalFmt

defaultColumn = 'ignore'

class HeadingFmtTable( DfTable ):
    def __init__( self, parent, df, headingCb, **kwargs ):
        self.df = df.applymap( str )
        self.headingCb = headingCb
        self.headVar = []
        shape = list( df.shape )
        shape[ 0 ] += 1
        Table.__init__( self, parent, shape=shape, **kwargs )
    
    def makeHeader( self, column, **kwargs ):
        var = tk.StringVar( self )
        var.set( defaultColumn )
        self.headVar.append( var )
        def cb( value, pos=column ):
            self.headingCb( value, pos )
        return tk.OptionMenu( self, var, defaultColumn, *internalFmt, command=cb )
    
    def makeCell( self, row, column, **kwargs ):
        if not row:
            return self.makeHeader( column, **kwargs )
        return DfTable.makeCell( self, row - 1, column, **kwargs )

class ImportLedgerWindow( tk.Toplevel ):
    def __init__( self, master, ledger, format, df, psize, *args, **kwargs ):
        tk.Toplevel.__init__( self, master, *args, **kwargs )
        self.ledger = ledger
        self.psize = psize
        self.df = df
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

    def build( self ):
        button = tk.Frame( self )
        button.pack( side=tk.BOTTOM, fill=tk.X )
        cancel = tk.Button( button, text="Cancel", command=self.destroy )
        cancel.pack( side=tk.RIGHT )
        self.confirm = tk.Button( button, text="Confirm", command=self.finalize, state=tk.DISABLED )
        self.confirm.pack( side=tk.RIGHT )

        scroll = Scrollable( self, horizontal=True, vertical=True )
        scroll.pack( side=tk.TOP, fill=tk.BOTH, expand=True )
        self.table = HeadingFmtTable( scroll, self.df.head( self.psize ), self.updateFmt )
        self.table.pack( side=tk.TOP, fill=tk.BOTH, expand=True )

def importLedgerCb( master, ledger, format, psize ):
    def cb( master=master, ledger=ledger, format=format, psize=psize ):
        f = tk.filedialog.askopenfilename()
        if not f:
            return
        df = pd.read_csv( f, index_col=None, header=None )
        window = ImportLedgerWindow( master, ledger, format, df, psize )
        master.wait_window( window )
    return cb