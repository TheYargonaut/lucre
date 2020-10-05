import tkinter as tk
from Scrollable import Scrollable
from Table import Table, DfTable
from List import ListView
from Group import Group
# window for editing a group

class EditGroupWindow( tk.Toplevel ):
    def __init__( self, master, group, ledger, psize, titleWidget, *args, **kwargs ):
        tk.Toplevel.__init__( self, master, *args, **kwargs )
        self.lastMask = None
        self.groupBack = group
        self.group = Group( **dict( group ) )
        self.ledger = ledger
        self.psize = psize
        self.titleWidget = titleWidget
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
                    c.config( background=self.ignored ) # unhighlight row
        self.lastMask = mask
    
    def finalize( self ):
        self.groupBack.whitelist = self.group.whitelist
        self.groupBack.blacklist = self.group.blacklist
        self.groupBack.negate = self.groupBack.negate
        self.groupBack.title = self.group.title
        self.titleWidget.config( text=self.group.title )
        self.ledger.updateCb( self.ledger.df )
        self.destroy()
        
    def whiteListCb( self, idx, txt ):
        self.group.whitelist[ idx ] = txt
        self.matchListCb()
    
    def blackListCb( self, idx, txt ):
        self.group.blacklist[ idx ] = txt
        self.matchListCb()
    
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
        whiteList = ListView( whiteScroll, self.group.whitelist, '+', self.whiteListCb )
        whiteList.pack()
        blackLabel = tk.Label( listFrame, text='blacklist' )
        blackLabel.grid( row=2, column=0, sticky=tk.NSEW )
        blackScroll = Scrollable( listFrame, vertical=True )
        blackScroll.grid( row=3, column=0, sticky=tk.NSEW )
        blackList = ListView( blackScroll, self.group.blacklist, '+', self.blackListCb )
        blackList.pack()

        button = tk.Frame( self )
        button.grid( row=1, column=0, columnspan=2, sticky=tk.E )
        cancel = tk.Button( button, text="Cancel", command=self.destroy )
        cancel.pack( side=tk.RIGHT )
        confirm = tk.Button( button, text="Confirm", command=self.finalize )
        confirm.pack( side=tk.RIGHT )

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

def editGroupCb( master, group, ledger, psize, titleWidget ):
    def cb( master=master, group=group, ledger=ledger, psize=psize, titleWidget=titleWidget ):
        window = EditGroupWindow( master, group, ledger, psize, titleWidget )
        master.wait_window( window )
    return cb