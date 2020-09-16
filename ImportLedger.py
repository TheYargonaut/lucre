# dialog window to import ledger
import tkinter as tk
import pandas as pd
from Scrollable import Scrollable
from Table import tableFromDf
from Ledger import knownFmt

defaultColumn = 'ignore'

def importLedgerCb( master, ledger ):
    
    def cb( master=master, ledger=ledger ):
        # choose file
        f = tk.filedialog.askopenfilename()
        if not f:
            return
        df = pd.read_csv( f, index_col=None, header=None )

        # preview and TODO choose columns, gatekeep confirmation
        top = tk.Toplevel( master )

        buttons = tk.Frame( top )
        cancelButton = tk.Button( buttons, text="Cancel", command=top.destroy )
        headerFmt = []
        def confirmCb( df=df, ledger=ledger ):
            fmt = [ str( i ) if name == defaultColumn else name for i, name in enumerate( headerFmt ) ]
            df.columns = fmt
            ledger.add( df )
            top.destroy()
        confirmButton = tk.Button( buttons, text="Confirm", command=confirmCb, state=tk.DISABLED )

        scroll = Scrollable( top, horizontal=True, vertical=True)
        scroll.pack( side=tk.TOP, fill=tk.BOTH, expand=True )
        table = tableFromDf( scroll, df, header=True )
        
        # replace top row with dropdowns for setting columns
        headerRow = []
        headerVar = []
        for i, cell in enumerate( table.cells[ 0 ] ):
            headerFmt.append( defaultColumn )
            cell.destroy()
            var = tk.StringVar( table )
            var.set( defaultColumn )
            def colCb( value, pos=i ):
                headerFmt[ pos ] = value
                if all( headerFmt.count( name ) == 1 for name in knownFmt[ 'internal' ] ):
                    confirmButton.configure( state=tk.NORMAL )
                else:
                    confirmButton.configure( state=tk.DISABLED )
            menu = tk.OptionMenu( table, var, defaultColumn, *knownFmt[ 'internal' ], command=colCb )
            menu.grid( row=0, column=i )
            headerRow.append( menu )
            headerVar.append( var )
        table.cells[ 0 ] = headerRow

        table.pack( side=tk.TOP, fill=tk.BOTH, expand=True )
        buttons.pack( side=tk.BOTTOM, fill=tk.X )
        cancelButton.pack( side=tk.RIGHT )
        confirmButton.pack( side=tk.RIGHT )
        master.wait_window( top )
    return cb