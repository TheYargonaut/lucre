from Viewer import Viewer
from ViewLedgerWidget import ViewLedgerWidget

import tkinter as tk

# window for browsing the ledger

class ViewLedgerWindow( tk.Toplevel, Viewer ):
    def __init__( self, master, group, ledger, *args, **kwargs ):
        tk.Toplevel.__init__( self, master, *args, **kwargs )
        Viewer.__init__( self, backer=[ group, ledger ] )
        self.title = 'browse ledger'
        self.group = group
        self.ledger = ledger

        self.view = None
        self.build()
    
    def onUpdate( self ):
        self.updateCb( self.view )
    
    def updateCb( self, view ):
        df = self.ledger.df.head( len( view ) )
        mask = [ group.filter( df ) for group in self.group.groups.values() ]

        for row in range( len( view ) ):
            for m, g in zip( mask, self.group.groups.values() ):
                if m.iloc[ row ]:
                    view.highlightRow( row, g.color )
                    break
    
    def build( self ):
        self.view = ViewLedgerWidget( self, self.ledger, self.updateCb )
        self.view.pack()

def viewLedgerCb( master, group, ledger ):
    def cb( master=master, group=group, ledger=ledger ):
        window = ViewLedgerWindow( master, group, ledger )
        master.wait_window( window )
    return cb