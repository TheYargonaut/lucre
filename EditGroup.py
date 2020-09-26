import tkinter as tk
from Scrollable import Scrollable
from Table import Table, DfTable
# window for editing a group

class EditGroupWindow( tk.Toplevel ):
    def __init__( self, master, group, ledger, psize, *args, **kwargs ):
        tk.Toplevel.__init__( self, master, *args, **kwargs )
        self.group = group
        self.ledger = ledger
        self.psize = psize
        self.build()
    
    def setListAddButton( self, table ):
        addButton = tk.Button( table, text='+' )
        def cb( button=addButton, table=table ):
            addButton.grid( row=1 + len( table.cells ), column=0, sticky=tk.NSEW )
            table.appendRow()
        addButton.config( command=cb )
        addButton.grid( row=len( table.cells ), column=0, sticky=tk.NSEW )

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
        listFrame.grid_rowconfigure( 0, weight=1 )
        listFrame.grid_rowconfigure( 1, weight=1 )
        listFrame.grid_columnconfigure( 0, weight=1 )
        
        doneButton = tk.Button( listFrame, text="Done", command=self.destroy )
        doneButton.grid( row=3, column=0, sticky=tk.NSEW )
        whiteScroll = Scrollable( listFrame, vertical=True )
        whiteScroll.grid( row=0, column=0, sticky=tk.NSEW )
        whiteList = Table( whiteScroll, ( 2, 1 ) )
        self.setListAddButton( whiteList )
        whiteList.pack()
        blackScroll = Scrollable( listFrame, vertical=True )
        blackScroll.grid( row=1, column=0, sticky=tk.NSEW )
        blackList = Table( blackScroll, ( 2, 1 ) )
        self.setListAddButton( blackList )
        blackList.pack()

        nameFrame = tk.Frame( mainFrame )
        nameFrame.grid( row=0, column=0, sticky=tk.NSEW )
        self.nameVar = tk.StringVar( nameFrame )
        self.nameVar.trace( 'w', self.nameCb )
        name = tk.Entry( nameFrame, textvariable=self.nameVar, exportselection=0 )
        name.pack( side=tk.LEFT, fill=tk.X, expand=True )
        styleVar = tk.StringVar( nameFrame )
        styleVar.set( "income" )
        style = tk.OptionMenu( nameFrame, styleVar, "income", "expense", command=self.expenseCb )
        style.pack( side=tk.RIGHT, fill=tk.NONE, expand=False )

        scroll = Scrollable( mainFrame, True, True )
        preview = DfTable( scroll, self.ledger.df )
        preview.pack( fill=tk.BOTH, expand=True )
        scroll.grid( row=1, column=0, sticky=tk.NE + tk.S )

def editGroupCb( master, group, ledger, psize ):
    def cb( master=master, group=group, ledger=ledger, psize=psize ):
        window = EditGroupWindow( master, group, ledger, psize )
        master.wait_window( window )
    return cb