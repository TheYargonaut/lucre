import tkinter as tk
from ViewLedgerWidget import ViewLedgerWidget

# window for browsing the ledger

class ViewLedgerWindow( tk.Toplevel ):
    def __init__( self, master, group, ledger, *args, **kwargs ):
        tk.Toplevel.__init__( self, master, *args, **kwargs )
        self.title = 'browse ledger'
        self.group = group
        self.ledger = ledger

        self.view = None
        self.build()
    
    def updateCb( self, view ):
        df = self.ledger.head( len( view ) )
        mask = [ group.filter( df ) for group in self.group.values() ]

        for row in range( len( view ) ):
            for m, g in zip( mask, self.group.values() ):
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