from Ledger import internalFmt
from Scrollable import Scrollable
from Table import DfTable, Table
from tkinter import ttk
import pandas as pd
import tkinter as tk
from Tooltip import Tooltip

defaultColumn = 'ignore'
prevLens = [ 10, 25, 100 ]

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
        def cb( *args, pos=column ):
            self.headingCb( var.get(), pos )
        var.trace( 'w', cb )
        self.headVar.append( var )
        return ttk.OptionMenu( self, var, defaultColumn, defaultColumn, *internalFmt )
    
    def makeCell( self, row, column, **kwargs ):
        if not row:
            return self.makeHeader( column, **kwargs )
        return DfTable.makeCell( self, row - 1, column, **kwargs )

class ImportLedgerWindow( tk.Toplevel ):
    def __init__( self, master, ledger, format, df, psize, *args, **kwargs ):
        tk.Toplevel.__init__( self, master, *args, **kwargs )
        self.ledger = ledger
        self.format = format
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
        if self.fmtFlag.get():
            self.format.formats[ self.fmtTitleVar.get() ] = fmt
        self.destroy()
    
    def updateFmt( self, value, pos ):
        if value in internalFmt:
            for f, h in zip( self.headerFmt, self.table.headVar ):
                if f == value:
                    h.set( 'ignore' )
        self.headerFmt[ pos ] = value
        if all( self.headerFmt.count( name ) == 1 for name in internalFmt ):
            if self.tooltip:
                self.confirm.configure( state=tk.NORMAL )
                self.tooltip.destroy()
                self.tooltip = None
        else:
            if self.tooltip is None:
                self.tooltip = Tooltip( self.confirm, "label columns to import" )
                self.confirm.configure( state=tk.DISABLED )
    
    def resizePreview( self, size ):
        if self.table is not None:
            self.table.destroy()
        self.table = HeadingFmtTable( self.scroll, self.df.head( int( size ) ), self.updateFmt )
        self.table.pack( side=tk.TOP, fill=tk.BOTH, expand=True )
    
    def importFormatCb( self, choice ):
        if choice == "New":
            self.fmtSave.pack( side=tk.LEFT )
            self.fmtTitle.pack( side=tk.LEFT, fill=tk.X, expand=True )
            for c, hdr in zip( self.table.cells[ 0 ], self.table.headVar ):
                hdr.set( defaultColumn )
                c.configure( state="enabled" )
            return
        self.fmtSave.pack_forget()
        self.fmtTitle.pack_forget()
        self.fmtFlag.set( 0 )
        for c, hdr, label in zip( self.table.cells[ 0 ], self.table.headVar, self.format.formats[ choice ] ):
            c.configure( state="disabled" )
            hdr.set( label if label in internalFmt else defaultColumn )
        # set up import

    def build( self ):
        forms = ttk.Frame( self )
        forms.pack( side=tk.TOP, fill=tk.X, expand=True )
        fmtVar = tk.StringVar( forms )
        fmtMenu = ttk.OptionMenu( forms, fmtVar, "New", "New", *[ k for k, f in self.format.formats.items() if len( f ) == self.df.shape[ 1 ] ], command=self.importFormatCb )
        fmtMenu.pack( side=tk.LEFT )
        self.fmtFlag = tk.IntVar( forms )
        self.fmtFlag.set( 0 )
        self.fmtSave = ttk.Checkbutton( forms, variable=self.fmtFlag, text="Save Format As" )
        self.fmtSave.pack( side=tk.LEFT )
        self.fmtTitleVar = tk.StringVar( forms )
        self.fmtTitleVar.set( "Untitled" )
        self.fmtTitle = ttk.Entry( forms, textvariable=self.fmtTitleVar )
        self.fmtTitle.pack( side=tk.LEFT, fill=tk.X, expand=True )

        button = ttk.Frame( self )
        button.pack( side=tk.BOTTOM, fill=tk.X )
        cancel = ttk.Button( button, text="Cancel", command=self.destroy )
        cancel.pack( side=tk.RIGHT )
        self.confirm = ttk.Button( button, text="Confirm", command=self.finalize, state=tk.DISABLED )
        self.confirm.pack( side=tk.RIGHT )
        self.tooltip = Tooltip( self.confirm, "label columns to import" )
        prevLenMenu = ttk.OptionMenu( button, tk.StringVar( button ), str( self.psize ), *[ str( p ) for p in prevLens if p < self.df.shape[ 0 ] ], self.df.shape[ 0 ], command=self.resizePreview )
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