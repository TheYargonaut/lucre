import tkinter as tk
from tkinter.colorchooser import askcolor, Chooser
from tkinter import ttk
from Scrollable import Scrollable
from Table import DfTable
from List import ListView
from Group import Group
# window for editing a group

prevLens = [ 10, 25, 100 ]

class EditGroupWindow( tk.Toplevel ):
    def __init__( self, master, group, ledger, psize, titleWidget, *args, **kwargs ):
        tk.Toplevel.__init__( self, master, *args, **kwargs )
        self.title( "edit group" )
        self.lastMask = None
        self.groupBack = group
        self.group = Group( **dict( group ) )
        self.ledger = ledger
        self.psize = psize
        self.titleWidget = titleWidget
        self.highlight = "white"
        self.ignored = "#E00E00E00" # gray
        self.table = None
        self.build()
        self.matchListCb()
    
    def matchListCb( self, *args ):
        'set the highlights when group lists change; modify ones that actually change'
        mask = self.group.filter( self.ledger.df )
        if self.lastMask is None:
            self.lastMask = ~mask
        for r, m, l in zip( self.table.cells, mask, self.lastMask ):
            for c in r:
                c.config( disabledbackground=self.highlight if m else self.ignored )
        self.lastMask = mask
    
    def finalize( self ):
        self.groupBack.whitelist = [ r for r in self.group.whitelist if r ]
        self.groupBack.blacklist = [ r for r in self.group.blacklist if r ]
        self.groupBack.negate = self.group.negate
        self.groupBack.title = self.group.title
        self.groupBack.color = self.group.color
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
    
    def colorCb( self ):
        self.group.color = askcolor( self.group.color, parent=self )[ 1 ]
        self.color.config( fg=self.group.color )
    
    def resizePreview( self, size ):
        if self.table is not None:
            self.table.destroy()
            self.table = None
        self.table = DfTable( self.scroll, self.ledger.df.head( int( size ) ) )
        self.table.pack( side=tk.TOP, fill=tk.BOTH, expand=True )
        self.matchListCb()

    def build( self ):
        self.grid_rowconfigure( 0, weight=1 )
        self.grid_columnconfigure( 0, weight=1 )
        mainFrame = ttk.Frame( self )
        mainFrame.grid( row=0, column=0, sticky=tk.NSEW )
        mainFrame.grid_rowconfigure( 1, weight=1 )
        mainFrame.grid_columnconfigure( 0, weight=1 )
        listFrame = ttk.Frame( self )
        listFrame.grid( row=0, column=1, sticky=tk.NSEW )
        listFrame.grid_rowconfigure( 0, weight=1 )
        listFrame.grid_rowconfigure( 1, weight=1 )
        listFrame.grid_columnconfigure( 0, weight=1 )
        
        whiteFrame = ttk.Frame( listFrame )
        whiteFrame.grid( row=0, column=0, sticky=tk.NSEW )
        whiteLabel = tk.Label( whiteFrame, text='whitelist' )
        whiteLabel.pack( side=tk.TOP, fill=tk.X )
        whiteScroll = Scrollable( whiteFrame, vertical=True )
        whiteScroll.pack( side=tk.TOP, fill=tk.BOTH )
        whiteList = ListView( whiteScroll, self.group.whitelist, '+', self.whiteListCb )
        whiteList.pack()
        blackFrame = ttk.Frame( listFrame )
        blackFrame.grid( row=1, column=0, sticky=tk.NSEW )
        blackLabel = tk.Label( blackFrame, text='blacklist' )
        blackLabel.pack( side=tk.TOP, fill=tk.X )
        blackScroll = Scrollable( blackFrame, vertical=True )
        blackScroll.pack( side=tk.TOP, fill=tk.BOTH )
        blackList = ListView( blackScroll, self.group.blacklist, '+', self.blackListCb )
        blackList.pack()

        button = ttk.Frame( self )
        button.grid( row=1, column=0, columnspan=2, sticky=tk.W + tk.E )
        cancel = ttk.Button( button, text="Cancel", command=self.destroy )
        cancel.pack( side=tk.RIGHT )
        confirm = ttk.Button( button, text="Confirm", command=self.finalize )
        confirm.pack( side=tk.RIGHT )
        prevLenMenu = ttk.OptionMenu( button, tk.StringVar( button ), str( self.psize ), *[ str( p ) for p in prevLens if p < self.ledger.df.shape[ 0 ] ], self.ledger.df.shape[ 0 ], command=self.resizePreview )
        prevLenMenu.pack( side=tk.LEFT )

        nameFrame = ttk.Frame( mainFrame )
        nameFrame.grid( row=0, column=0, sticky=tk.NSEW )
        self.color = tk.Button( nameFrame, text="\u2B1B", command=self.colorCb, width=3 )
        self.color.config( fg=self.group.color )
        self.color.pack( side=tk.LEFT, fill=tk.NONE, expand=False )
        self.nameVar = tk.StringVar( nameFrame )
        self.nameVar.set( self.group.title )
        self.nameVar.trace( 'w', self.nameCb )
        name = ttk.Entry( nameFrame, textvariable=self.nameVar, exportselection=0 )
        name.pack( side=tk.LEFT, fill=tk.X, expand=True )
        style = ttk.OptionMenu( nameFrame, tk.StringVar( nameFrame ), ( "expense" if self.group.negate else "income" ), "income", "expense", command=self.expenseCb )
        style.pack( side=tk.RIGHT, fill=tk.NONE, expand=False )

        self.scroll = Scrollable( mainFrame, True, True )
        self.scroll.grid( row=1, column=0, sticky=tk.NE + tk.S )
        self.resizePreview( self.psize )

def editGroupCb( master, group, ledger, psize, titleWidget ):
    def cb( master=master, group=group, ledger=ledger, psize=psize, titleWidget=titleWidget ):
        window = EditGroupWindow( master, group, ledger, psize, titleWidget )
        master.wait_window( window )
    return cb