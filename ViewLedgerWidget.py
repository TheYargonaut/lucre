import tkinter as tk
from tkinter import ttk
from Scrollable import Scrollable
from Table import DfTable
# window for browsing the ledger

lengthList = [ 10, 25, 100, 250, 1000 ]

class ViewLedgerWidget( ttk.Frame ):
    def __init__( self, master, ledger, lenCb=lambda:None, length=lengthList[ 0 ], *args, **kwargs ):
        ttk.Frame.__init__( self, master, *args, **kwargs )
        self.ledger = ledger
        self.lenCb = lenCb
        self.length = length

        self.lengthList = [
            str( l ) for l in lengthList if l < self.ledger.shape[ 0 ]
        ] + [ self.ledger.shape[ 0 ] ]

        self.scroll = None
        self.table = None
        self.build()
    
    def highlightRow( self, idx, color ):
        self.table.configRowColor( idx, color )
    
    def resizePreview( self, size ):
        self.length = int( size )
        if self.table is not None:
            self.table.destroy()
            self.table = None
        self.table = DfTable( self.scroll, self.ledger.head( self.length ) )
        self.table.pack( side=tk.TOP, fill=tk.BOTH, expand=True )
        self.lenCb( self )
    
    def build( self ):
        self.scroll = Scrollable( self, True, True )
        self.scroll.pack( side=tk.TOP, fill=tk.BOTH )
        
        self.controlFrame = ttk.Frame( self )
        self.controlFrame.pack( side=tk.BOTTOM, fill=tk.X )


        self.lengthVar = tk.StringVar( self.controlFrame )
        self.lengthVar.set( str( self.length ) )
        self.resizePreview( self.length )
        prevLenMenu = ttk.OptionMenu(
            self.controlFrame,
            self.lengthVar,
            None,
            *self.lengthList,
            command=self.resizePreview
        )
        prevLenMenu.pack( side=tk.LEFT )
    
    def __len__( self ):
        return self.length