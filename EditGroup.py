import tkinter as tk
from Scrollable import Scrollable
from Table import Table, DfTable
from List import ListView
# window for editing a group

class EditGroupWindow( tk.Toplevel ):
    def __init__( self, master, group, ledger, psize, *args, **kwargs ):
        tk.Toplevel.__init__( self, master, *args, **kwargs )
        self.lastMask = None
        self.group = group
        self.ledger = ledger
        self.psize = psize
        self.highlight = "white"
        self.ignored = "#E00E00E00" # gray
        self.build()
        self.matchListCb()
    
    def matchListCb( self, *args ):
        'set the highlights when group lists change; modify ones that actually change'
        mask = self.group.filter( self.ledger.df )
        if self.lastMask is None:
            self.lastMask = ~mask
        for r, m, l in zip( self.preview.cells, mask, self.lastMask ):
            if m and not l:
                for c in r:
                    c.config( background=self.highlight ) # highlight row
            if l and not m:
                for c in r:
                    c.config( background=self.ignored ) # highlight row
        self.lastMask = mask
    
    def nameCb( self, *args ):
        self.group.title = self.nameVar.get()
    
    def expenseCb( self, value ):
        self.group.negate = value == 'expense'

    def build( self ):
        self.grid_rowconfigure( 0, weight=1 )
        self.grid_columnconfigure( 0, weight=1 )
        mainFrame = tk.Frame( self )
        mainFrame.grid( row=0, column=0, sticky=tk.NSEW )
        mainFrame.grid_rowconfigure( 1, weight=1 )
        mainFrame.grid_columnconfigure( 0, weight=1 )
        listFrame = tk.Frame( self )
        listFrame.grid( row=0, column=1, sticky=tk.NSEW )
        listFrame.grid_rowconfigure( 1, weight=1 )
        listFrame.grid_rowconfigure( 3, weight=1 )
        listFrame.grid_columnconfigure( 0, weight=1 )
        
        whiteLabel = tk.Label( listFrame, text='whitelist' )
        whiteLabel.grid( row=0, column=0, sticky=tk.NSEW )
        whiteScroll = Scrollable( listFrame, vertical=True )
        whiteScroll.grid( row=1, column=0, sticky=tk.NSEW )
        whiteList = ListView( whiteScroll, self.group.whitelist, '+', self.matchListCb )
        whiteList.pack()
        blackLabel = tk.Label( listFrame, text='blacklist' )
        blackLabel.grid( row=2, column=0, sticky=tk.NSEW )
        blackScroll = Scrollable( listFrame, vertical=True )
        blackScroll.grid( row=3, column=0, sticky=tk.NSEW )
        blackList = ListView( blackScroll, self.group.blacklist, '+', self.matchListCb )
        blackList.pack()
        doneButton = tk.Button( listFrame, text="Done", command=self.destroy )
        doneButton.grid( row=5, column=0, sticky=tk.NSEW )

        nameFrame = tk.Frame( mainFrame )
        nameFrame.grid( row=0, column=0, sticky=tk.NSEW )
        self.nameVar = tk.StringVar( nameFrame )
        self.nameVar.set( self.group.title )
        self.nameVar.trace( 'w', self.nameCb )
        name = tk.Entry( nameFrame, textvariable=self.nameVar, exportselection=0 )
        name.pack( side=tk.LEFT, fill=tk.X, expand=True )
        styleVar = tk.StringVar( nameFrame )
        styleVar.set( "expense" if self.group.negate else "income" )
        style = tk.OptionMenu( nameFrame, styleVar, "income", "expense", command=self.expenseCb )
        style.pack( side=tk.RIGHT, fill=tk.NONE, expand=False )

        scroll = Scrollable( mainFrame, True, True )
        self.preview = DfTable( scroll, self.ledger.df.head( self.psize ) )
        self.preview.pack( fill=tk.BOTH, expand=True )
        scroll.grid( row=1, column=0, sticky=tk.NE + tk.S )

def editGroupCb( master, group, ledger, psize ):
    def cb( master=master, group=group, ledger=ledger, psize=psize ):
        window = EditGroupWindow( master, group, ledger, psize )
        master.wait_window( window )
    return cb