import tkinter as tk
from tkinter import ttk
from Scrollable import Scrollable
from Table import DfTable
# window for browsing the ledger

prevLens = [ 10, 25, 100 ]

class ViewLedgerWindow( tk.Toplevel ):
    def __init__( self, master, group, ledger, *args, **kwargs ):
        tk.Toplevel.__init__( self, master, *args, **kwargs )
        self.title = 'browse ledger'
        self.group = group
        self.ledger = ledger

        self.table = None
        self.psize = prevLens[ 1 ]
        self.build()
    
    def resizePreview( self, size ):
        if self.table is not None:
            self.table.destroy()
            self.table = None
        self.table = DfTable( self.scroll, self.ledger.head( int( size ) ) )
        self.table.pack( side=tk.TOP, fill=tk.BOTH, expand=True )

        for row in range( self.table.shape[ 0 ] ):
            for group in self.group.values():
                if group.filter( self.ledger.iloc[ row:row+1 ] ).all():
                    self.table.configRowColor( row, group.color )
                    break
    
    def build( self ):
        self.scroll = Scrollable( self, True, True )
        self.scroll.pack( side=tk.TOP, fill=tk.BOTH )
        
        self.controlFrame = ttk.Frame( self )
        self.controlFrame.pack( side=tk.BOTTOM, fill=tk.X )

        self.resizePreview( self.psize )
        prevLenMenu = ttk.OptionMenu(
            self.controlFrame,
            tk.StringVar( self.controlFrame ),
            str( self.psize ),
            *[ str( p ) for p in prevLens if p < self.ledger.shape[ 0 ] ], self.ledger.shape[ 0 ],
            command=self.resizePreview
        )
        prevLenMenu.pack( side=tk.LEFT )

def viewLedgerCb( master, group, ledger ):
    def cb( master=master, group=group, ledger=ledger ):
        window = ViewLedgerWindow( master, group, ledger )
        master.wait_window( window )
    return cb