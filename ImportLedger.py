# dialog window to import ledger
import tkinter as tk
import pandas as pd
from Scrollable import Scrollable
from Table import tableFromDf
from Ledger import internalFmt

defaultColumn = 'ignore'

class ImportLedgerWindow( tk.Toplevel ):
    def __init__( self, master, ledger, df, *args, **kwargs ):
        tk.Toplevel.__init__( self, master, *args, **kwargs )
        self.ledger = ledger
        self.df = df
        self.headerFmt = []
        self.build()
    
    def finalize( self ):
        fmt = [ str( i ) if name == defaultColumn else name
                for i, name in enumerate( self.headerFmt ) ]
        self.df.columns = fmt
        self.ledger.add( self.df )
        self.destroy()
    
    def updateFmt( self, value, pos ):
        self.headerFmt[ pos ] = value
        if all( self.headerFmt.count( name ) == 1 for name in internalFmt ):
            self.confirm.configure( state=tk.NORMAL )
        else:
            self.confirm.configure( state=tk.DISABLED )

    def setTableHeader( self, table ):
        'replace top row with dropdowns for setting column names'
        headerRow = []
        for i, cell in enumerate( table.cells[ 0 ] ):
            self.headerFmt.append( defaultColumn )
            cell.destroy()
            var = tk.StringVar( table )
            var.set( defaultColumn )
            colCb = lambda value, pos=i : self.updateFmt( value, pos )
            menu = tk.OptionMenu( table, var, defaultColumn, *internalFmt, command=colCb )
            menu.grid( row=0, column=i )
            headerRow.append( menu )
        table.cells[ 0 ] = headerRow

    def build( self ):
        button = tk.Frame( self )
        button.pack( side=tk.BOTTOM, fill=tk.X )
        cancel = tk.Button( button, text="Cancel", command=self.destroy )
        cancel.pack( side=tk.RIGHT )
        self.confirm = tk.Button( button, text="Confirm", command=self.finalize, state=tk.DISABLED )
        self.confirm.pack( side=tk.RIGHT )

        scroll = Scrollable( self, horizontal=True, vertical=True )
        scroll.pack( side=tk.TOP, fill=tk.BOTH, expand=True )
        table = tableFromDf( scroll, self.df, header=True )
        self.setTableHeader( table )
        table.pack( side=tk.TOP, fill=tk.BOTH, expand=True )

def importLedgerCb( master, ledger ):
    def cb( master=master, ledger=ledger ):
        f = tk.filedialog.askopenfilename()
        if not f:
            return
        df = pd.read_csv( f, index_col=None, header=None )
        window = ImportLedgerWindow( master, ledger, df )
        master.wait_window( window )
    return cb